/**
 * Controller - Handles communication between frontend and Python backend (Eel)
 * All exposed functions that can be called from Python
 */

// Utility for safe DOM manipulation
const DOMUtils = {
  /**
   * Safely get element by selector
   */
  getElement(selector) {
    const element = $(selector);
    if (element.length === 0) {
      console.warn(`Element not found: ${selector}`);
      return null;
    }
    return element;
  },

  /**
   * Safely set element attribute
   */
  setAttr(selector, attr, value) {
    const element = this.getElement(selector);
    if (element) {
      element.attr(attr, value);
    }
  },

  /**
   * Safely add class with animation
   */
  addClass(selector, className) {
    const element = this.getElement(selector);
    if (element) {
      element.addClass(className);
    }
  },

  /**
   * Safely scroll element to bottom
   */
  scrollToBottom(selector) {
    const element = document.getElementById(selector);
    if (element) {
      element.scrollTop = element.scrollHeight;
    }
  }
};

/**
 * Message Display Functions
 */

// Display a message with animation
eel.expose(DisplayMessage);
function DisplayMessage(message) {
  try {
    if (!message) {
      console.warn('DisplayMessage called with empty message');
      return;
    }

    const messageElement = DOMUtils.getElement(".siri-message li:first");
    if (messageElement) {
      messageElement.text(message);
      
      const siriMessage = DOMUtils.getElement(".siri-message");
      if (siriMessage && typeof siriMessage.textillate === 'function') {
        siriMessage.textillate("start");
      }
    }
  } catch (error) {
    console.error('Error in DisplayMessage:', error);
  }
}

/**
 * UI State Management Functions
 */

// Show the main hood interface
eel.expose(ShowHood);
function ShowHood() {
  try {
    DOMUtils.setAttr("#Oval", "hidden", false);
    DOMUtils.setAttr("#SiriWave", "hidden", true);
  } catch (error) {
    console.error('Error in ShowHood:', error);
  }
}

// Hide loader and show face authentication
eel.expose(hideLoader);
function hideLoader() {
  try {
    DOMUtils.setAttr("#Loader", "hidden", true);
    DOMUtils.setAttr("#FaceAuth", "hidden", false);
  } catch (error) {
    console.error('Error in hideLoader:', error);
  }
}

// Hide face authentication and show success animation
eel.expose(hideFaceAuth);
function hideFaceAuth() {
  try {
    DOMUtils.setAttr("#FaceAuth", "hidden", true);
    DOMUtils.setAttr("#FaceAuthSuccess", "hidden", false);
  } catch (error) {
    console.error('Error in hideFaceAuth:', error);
  }
}

// Hide success animation and show greeting
eel.expose(hideFaceAuthSuccess);
function hideFaceAuthSuccess() {
  try {
    DOMUtils.setAttr("#FaceAuthSuccess", "hidden", true);
    DOMUtils.setAttr("#HelloGreet", "hidden", false);
  } catch (error) {
    console.error('Error in hideFaceAuthSuccess:', error);
  }
}

// Hide start page and display blob with animation
eel.expose(hideStart);
function hideStart() {
  try {
    DOMUtils.setAttr("#Start", "hidden", true);

    setTimeout(() => {
      DOMUtils.addClass("#Oval", "animate__animated animate__zoomIn");
    }, 1000);
    
    setTimeout(() => {
      DOMUtils.setAttr("#Oval", "hidden", false);
    }, 1000);
  } catch (error) {
    console.error('Error in hideStart:', error);
  }
}

/**
 * Chat Message Functions
 */

// Add sender message to chat
eel.expose(senderText);
function senderText(message) {
  try {
    const chatBox = document.getElementById("chat-canvas-body");
    if (!chatBox) {
      console.warn('Chat box not found');
      return;
    }

    if (!message || message.trim() === "") {
      console.warn('senderText called with empty message');
      return;
    }

    // Sanitize message to prevent XSS
    const sanitizedMessage = $('<div>').text(message).html();

    // Create message element
    const messageHTML = `
      <div class="row justify-content-end mb-4">
        <div class="width-size">
          <div class="sender_message">${sanitizedMessage}</div>
        </div>
      </div>`;

    chatBox.innerHTML += messageHTML;
    DOMUtils.scrollToBottom("chat-canvas-body");
  } catch (error) {
    console.error('Error in senderText:', error);
  }
}

// Add receiver message to chat
eel.expose(receiverText);
function receiverText(message) {
  try {
    const chatBox = document.getElementById("chat-canvas-body");
    if (!chatBox) {
      console.warn('Chat box not found');
      return;
    }

    if (!message || message.trim() === "") {
      console.warn('receiverText called with empty message');
      return;
    }

    // Sanitize message to prevent XSS
    const sanitizedMessage = $('<div>').text(message).html();

    // Create message element
    const messageHTML = `
      <div class="row justify-content-start mb-4">
        <div class="width-size">
          <div class="receiver_message">${sanitizedMessage}</div>
        </div>
      </div>`;

    chatBox.innerHTML += messageHTML;
    DOMUtils.scrollToBottom("chat-canvas-body");
  } catch (error) {
    console.error('Error in receiverText:', error);
  }
}

/**
 * Additional Helper Functions
 */

// Clear chat history
eel.expose(clearChat);
function clearChat() {
  try {
    const chatBox = document.getElementById("chat-canvas-body");
    if (chatBox) {
      chatBox.innerHTML = '';
      console.log('Chat history cleared');
    }
  } catch (error) {
    console.error('Error in clearChat:', error);
  }
}

// Update status message
eel.expose(updateStatus);
function updateStatus(status) {
  try {
    const wishMessage = DOMUtils.getElement("#WishMessage li:first");
    if (wishMessage) {
      wishMessage.text(status);
    }
  } catch (error) {
    console.error('Error in updateStatus:', error);
  }
}

// Show notification
eel.expose(showNotification);
function showNotification(title, message, type = 'info') {
  try {
    // This could be enhanced with a proper notification system
    console.log(`[${type.toUpperCase()}] ${title}: ${message}`);
    
    // For now, using browser notification API if available
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification(title, {
        body: message,
        icon: '/frontend/assets/img/logo.ico'
      });
    }
  } catch (error) {
    console.error('Error in showNotification:', error);
  }
}

// Request notification permission
eel.expose(requestNotificationPermission);
function requestNotificationPermission() {
  if ('Notification' in window && Notification.permission !== 'granted') {
    Notification.requestPermission().then(permission => {
      console.log('Notification permission:', permission);
    });
  }
}

// Set assistant state (listening, processing, idle, etc.)
eel.expose(setAssistantState);
function setAssistantState(state) {
  try {
    const validStates = ['idle', 'listening', 'processing', 'speaking'];
    
    if (!validStates.includes(state)) {
      console.warn(`Invalid state: ${state}`);
      return;
    }

    // Remove all state classes
    const body = $('body');
    validStates.forEach(s => body.removeClass(`state-${s}`));
    
    // Add current state class
    body.addClass(`state-${state}`);
    
    console.log(`Assistant state changed to: ${state}`);
  } catch (error) {
    console.error('Error in setAssistantState:', error);
  }
}

// Show error message to user
eel.expose(showError);
function showError(errorMessage) {
  try {
    console.error('Backend error:', errorMessage);
    
    // Display error in chat if available
    const chatBox = document.getElementById("chat-canvas-body");
    if (chatBox) {
      const errorHTML = `
        <div class="row justify-content-center mb-4">
          <div class="width-size">
            <div class="error_message" style="
              padding: 12px 16px;
              border: 2px solid #ff0000;
              border-radius: 8px;
              background-color: rgba(255, 0, 0, 0.1);
              color: #ff6b6b;
              text-align: center;
            ">
              <i class="bi bi-exclamation-triangle"></i> ${$('<div>').text(errorMessage).html()}
            </div>
          </div>
        </div>`;
      chatBox.innerHTML += errorHTML;
      DOMUtils.scrollToBottom("chat-canvas-body");
    }
  } catch (error) {
    console.error('Error in showError:', error);
  }
}

// Enable/disable input controls
eel.expose(setInputEnabled);
function setInputEnabled(enabled) {
  try {
    const chatbox = DOMUtils.getElement("#chatbox");
    const micBtn = DOMUtils.getElement("#MicBtn");
    const sendBtn = DOMUtils.getElement("#SendBtn");
    
    if (chatbox) chatbox.prop('disabled', !enabled);
    if (micBtn) micBtn.prop('disabled', !enabled);
    if (sendBtn) sendBtn.prop('disabled', !enabled);
    
    console.log(`Input controls ${enabled ? 'enabled' : 'disabled'}`);
  } catch (error) {
    console.error('Error in setInputEnabled:', error);
  }
}

/**
 * Initialize controller
 */
$(document).ready(() => {
  console.log('Controller initialized');
  
  // Request notification permission on load
  if ('Notification' in window && Notification.permission === 'default') {
    setTimeout(requestNotificationPermission, 2000);
  }
});

/**
 * Export for testing/debugging
 */
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    DisplayMessage,
    ShowHood,
    senderText,
    receiverText,
    hideLoader,
    hideFaceAuth,
    hideFaceAuthSuccess,
    hideStart,
    clearChat,
    updateStatus,
    showNotification,
    setAssistantState,
    showError,
    setInputEnabled,
    DOMUtils
  };
}
