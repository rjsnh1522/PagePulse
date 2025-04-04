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
    async function getIPv4() {
        try {
            const res = await fetch("https://api.ipify.org?format=json");
            const data = await res.json();
            return data.ip;
        } catch {
            return "Unknown";
        }
    }

    // Get user's IPv6
    async function getIPv6() {
        try {
            const res = await fetch("https://api64.ipify.org?format=json");
            const data = await res.json();
            return data.ip;
        } catch {
            return "Unknown";
        }
    }

    async function getBrowserInfo() {
        if (navigator.userAgentData && navigator.userAgentData.brands) {
            const validBrands = navigator.userAgentData.brands
                .filter(b => !/^Not.?A.?Brand$/i.test(b.brand))
                .sort((a, b) => parseInt(b.version, 10) - parseInt(a.version, 10));

            const brand1 = validBrands[0]?.brand || "Unknown";
            const brand2 = validBrands[1]?.brand || null;
            const platform = navigator.userAgentData.platform || navigator.platform;

            return { brand1, brand2, platform };
        } else {
            const ua = navigator.userAgent;
            let brand = "Unknown";
            if (/chrome|crios|crmo/i.test(ua)) brand = 'Chrome';
            else if (/firefox|fxios/i.test(ua)) brand = 'Firefox';
            else if (/safari/i.test(ua) && !/chrome|crios|crmo|fxios/i.test(ua)) brand = 'Safari';
            else if (/edg/i.test(ua)) brand = 'Edge';
            else if (/opr|opera/i.test(ua)) brand = 'Opera';

            return {
                brand1: brand,
                brand2: null,
                platform: navigator.platform || "Unknown"
            };
        }
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

    async function prepareData(isExit){

        const [ipv4, ipv6, browserInfo] = await Promise.all([getIPv4(), getIPv6(), getBrowserInfo()]);
        const timeSpent = Math.round((Date.now() - startTime) / 1000);
        maxScrollPosition = Math.max(maxScrollPosition, getMaxScrollPosition());

        const data = {
            visitor_id: visitorId,
            visitor_session_id: visitorSessionId,
            ipv4:ipv4,
            ipv6:ipv6,
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
        return data

    }

     async function sendAnalytics(isExit=false, debugMessage = "") {
        console.log("sending isExit", isExit, "debugmessage", debugMessage)
        let data = await prepareData(isExit)
        console.log("data", data)
        const blob = new Blob([JSON.stringify(data)], { type: "application/json" });
        navigator.sendBeacon(API_URL, blob);
    }

    // Immediately track on page load
    document.addEventListener("DOMContentLoaded", () => {
        sendAnalytics(false)
    });

    document.addEventListener("visibilitychange", () => {
        if (document.visibilityState === "hidden"){
            sendAnalytics(true, "visibilitychange");
        }
    });

    // Continuous scroll tracking
    window.addEventListener("scroll", () => {
        maxScrollPosition = Math.max(maxScrollPosition, window.scrollY + window.innerHeight);
    });

    window.addEventListener("beforeunload", () => sendAnalytics(true, "beforeunload"));
    window.addEventListener("pagehide", () => sendAnalytics(true, "pagehide"));


})();
