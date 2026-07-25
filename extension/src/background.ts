/// <reference types="chrome"/>

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "investigate-link",
    title: "Investigate Link with PHOENIX",
    contexts: ["link"]
  });

  chrome.contextMenus.create({
    id: "investigate-text",
    title: "Investigate '%s' with PHOENIX",
    contexts: ["selection"]
  });
  
  console.log("PHOENIX Extension Installed and Context Menus created.");
});

chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  let contextType = "";
  let payload = "";

  if (info.menuItemId === "investigate-link" && info.linkUrl) {
    contextType = "URL";
    payload = info.linkUrl;
  } else if (info.menuItemId === "investigate-text" && info.selectionText) {
    contextType = "TEXT";
    payload = info.selectionText;
  }

  if (contextType && payload) {
    try {
      // We will need the auth token from storage
      const result = await chrome.storage.local.get(["phoenix_token"]);
      const token = result.phoenix_token;

      if (!token) {
        // Create a notification to login
        chrome.notifications.create({
          type: "basic",
          iconUrl: "icon.png",
          title: "PHOENIX",
          message: "Please login to the PHOENIX extension first."
        });
        return;
      }

      const response = await fetch("http://localhost:8000/api/v1/extension/investigate/quick", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
          url: contextType === "URL" ? payload : null,
          text: contextType === "TEXT" ? payload : null,
          context_type: contextType
        })
      });

      const data = await response.json();
      
      if (response.ok) {
        chrome.notifications.create({
          type: "basic",
          iconUrl: "icon.png", // would normally bundle an icon
          title: "Investigation Started",
          message: `Score: ${data.threat_score}. ID: ${data.investigation_id}`
        });
      } else {
        console.error("Investigation failed", data);
      }
    } catch (err) {
      console.error(err);
    }
  }
});
