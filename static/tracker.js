(function () {
    const API_URL = "http://localhost:8080/v1/analytics";

    const startTime = Date.now();
    let maxScrollPosition = 0;
    const visitorId = getVisitorId();
    const visitorSessionId = getVisitorSessionId();
    let hasSentUnload = false;
    let isSending = false;

    // Visitor ID (persistent)
    function getVisitorId() {
        let visitorId = localStorage.getItem("visitor_uid");
        if (!visitorId) {
            visitorId = crypto.randomUUID();
            localStorage.setItem("visitor_uid", visitorId);
        }
        return visitorId;
    }

    // Session ID (per page load)
    function getVisitorSessionId() {
        return crypto.randomUUID();
    }

    // Get user's IPv4
    function getIPv4() {
        return fetch("https://api.ipify.org?format=json")
            .then(res => res.json())
            .then(data => data.ip)
            .catch(() => "Unknown");
    }

    // Get user's IPv6
     function getIPv6() {
        return fetch("https://api64.ipify.org?format=json")
            .then(res => res.json())
            .then(data => data.ip)
            .catch(() => "Unknown");
    }

    function getBrowserInfo() {
        return new Promise((resolve) => {
            if (navigator.userAgentData && navigator.userAgentData.brands) {
                const validBrands = navigator.userAgentData.brands
                    .filter(b => !/^Not.?A.?Brand$/i.test(b.brand))
                    .sort((a, b) => parseInt(b.version, 10) - parseInt(a.version, 10));

                const brand1 = validBrands[0]?.brand || "Unknown";
                const brand2 = validBrands[1]?.brand || null;
                const platform = navigator.userAgentData.platform || navigator.platform;

                resolve({ brand1, brand2, platform });
            } else {
                const ua = navigator.userAgent;
                let brand = "Unknown";
                if (/chrome|crios|crmo/i.test(ua)) brand = 'Chrome';
                else if (/firefox|fxios/i.test(ua)) brand = 'Firefox';
                else if (/safari/i.test(ua) && !/chrome|crios|crmo|fxios/i.test(ua)) brand = 'Safari';
                else if (/edg/i.test(ua)) brand = 'Edge';
                else if (/opr|opera/i.test(ua)) brand = 'Opera';

                resolve({
                    brand1: brand,
                    brand2: null,
                    platform: navigator.platform || "Unknown"
                });
            }
        });
    }

    function getDevice(){
        const ua = navigator.userAgent;
        if (/mobile/i.test(ua)) return 'Mobile';
        if (/tablet|ipad|playbook|silk/i.test(ua)) return 'Tablet';
        return 'Desktop';
    }

    function getMaxScrollPosition() {
        return Math.min(maxScrollPosition, document.body.scrollHeight);
    }

    function prepareData(isExit) {

        return Promise.all([getIPv4(), getIPv6(), getBrowserInfo()]).then(([ipv4, ipv6, browserInfo]) => {
            const timeSpent = Math.round((Date.now() - startTime) / 1000);
            maxScrollPosition = Math.max(maxScrollPosition, getMaxScrollPosition());

            return {
                website_id: window.trackerWebsiteId,
                visitor_id: visitorId,
                visitor_session_id: visitorSessionId,
                ipv4: ipv4,
                ipv6: ipv6,
                current_page_url: window.location.href,
                current_page_path: window.location.pathname,
                domain_name: window.location.hostname,
                referrer: document.referrer || "Direct",
                user_agent: navigator.userAgent,
                browser_primary: browserInfo.brand1,
                browser_secondary: browserInfo.brand2,
                platform: browserInfo.platform,
                device: getDevice(),
                page_height: document.body.scrollHeight,
                scroll_depth: maxScrollPosition,
                session_duration: timeSpent,
                timestamp: new Date().toISOString(),
                event_type: isExit ? "onExit" : "onLoad",
                exit_timestamp: isExit ? new Date().toISOString() : null
            };
        });
    }

     function sendAnalytics(isExit = false, debugMessage = "") {
        return new Promise((resolve) => {
            console.log("sending isExit:", isExit, "| debugMessage:", debugMessage);
            prepareData(isExit).then(data => {
                console.log("data:", data, 'debugMessage', debugMessage);
                const blob = new Blob([JSON.stringify(data)], { type: "application/json" });
                let return_val = navigator.sendBeacon(API_URL, blob);
                console.log("after send beacon : ", 'send_beacon return',
                return_val, 'debugMessage:', debugMessage, 'isExit: ', isExit)
                resolve()
            }).catch(err => {
                console.error("Error preparing analytics data:", err);
                resolve(); // Still resolve on error
            });
        });
    }

    // Immediately track on page load
    document.addEventListener("DOMContentLoaded", () => {
        sendAnalytics(false, 'dom loaded')
    });

//    document.addEventListener("visibilitychange", () => {
//        if (document.visibilityState === "hidden"){
//            sendAnalytics(true, "visibilitychange");
//        }
//    });

    // Continuous scroll tracking
    window.addEventListener("scroll", () => {
        maxScrollPosition = Math.max(maxScrollPosition, window.scrollY + window.innerHeight);
    });

//    window.addEventListener("beforeunload", () => sendAnalytics(true, "beforeunload"));
    window.addEventListener("pagehide", (event) => {
        console.log("page hide", event)
        sendAnalytics(true, "pagehide")
    });


    document.addEventListener('click', function(e) {
        const link = e.target.closest('a');
        if (!link) return;

        const href = link.getAttribute('href');
        if (!href || href.startsWith('#') || href.startsWith('javascript:')) return;

        // Check if link is internal
        const isInternal = new URL(href, window.location.href).origin === window.location.origin;
        if (!isInternal) return;

        e.preventDefault();
        sendAnalytics(true, "link click").then(()=>{
            console.log("Analytics completed - now navigating");
            window.location.href = href;
        }).catch(err => {
            console.error("Analytics failed, navigating anyway", err);
            window.location.href = href;
        })
    }, true)


})();
