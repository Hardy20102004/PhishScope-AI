// Listens for messages from the background script or popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "GET_DOM_METADATA") {
    const metaTags = Array.from(document.getElementsByTagName('meta')).map(meta => ({
      name: meta.getAttribute('name') || meta.getAttribute('property'),
      content: meta.getAttribute('content')
    }));

    sendResponse({
      title: document.title,
      url: window.location.href,
      metaTags: metaTags,
      timestamp: new Date().toISOString()
    });
  }
  return true;
});
