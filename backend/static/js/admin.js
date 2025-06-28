// SMART-EN System - Basic JavaScript
console.log("SMART-EN System Backend - Static files loaded successfully");

// Basic utility functions
window.smartEN = {
  version: "1.0.0",
  apiBase: window.location.origin,

  formatDate: function (date) {
    return new Date(date).toLocaleDateString();
  },

  showMessage: function (message, type = "info") {
    console.log(`[${type.toUpperCase()}] ${message}`);
  },
};

// Initialize when DOM is ready
document.addEventListener("DOMContentLoaded", function () {
  console.log("SMART-EN System initialized");
});
