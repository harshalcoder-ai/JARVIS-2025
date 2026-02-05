/**
 * Main JavaScript for Jarvis AI Assistant Interface
 * Handles initialization, animations, and user interactions
 */

// Configuration object
const CONFIG = {
  textillate: {
    loop: true,
    speed: 1500,
    sync: true,
    in: { effect: "bounceIn" },
    out: { effect: "bounceOut" }
  },
  siriMessage: {
    loop: true,
    sync: true,
    in: { effect: "fadeInUp", sync: true },
    out: { effect: "fadeOutUp", sync: true }
  },
  siriWave: {
    width: 940,
    style: "ios9",
    amplitude: 1,
    speed: 0.30,
    height: 200,
    autostart: true,
    waveColor: "#ff0000",
    waveOffset: 0,
    rippleEffect: true,
    rippleColor: "#ffffff"
  },
  keyboard: {
    voiceActivationKey: "j",
    voiceActivationMeta: true
  }
};

// State management
const State = {
  isProcessing: false,
  chatModalOpen: false,
  siriWaveInstance: null
};

/**
 * Utility functions
 */
const Utils = {
  /**
   * Safely call eel functions with error handling
   */
  async callEel(fn, ...args) {
    try {
      if (typeof fn === 'function') {
        return await fn(...args);
      }
      console.warn('Eel function not available:', fn);
    } catch (error) {
      console.error('Error calling eel function:', error);
      this.showError('Communication error. Please try again.');
    }
  },

  /**
   * Show error message to user
   */
  showError(message) {
    // Could be enhanced with a toast notification system
    console.error(message);
    alert(message);
  },

  /**
   * Debounce function to limit rate of function calls
   */
  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  },

  /**
   * Toggle element visibility with animation
   */
  toggleElement(selector, show) {
    const element = $(selector);
    if (show) {
      element.attr("hidden", false).addClass("fade-in");
    } else {
      element.addClass("fade-out");
      setTimeout(() => {
        element.attr("hidden", true).removeClass("fade-in fade-out");
      }, 300);
    }
  }
};

/**
 * Animation Controller
 */
const AnimationController = {
  /**
   * Initialize all text animations
   */
  initTextAnimations() {
    try {
      // Main greeting text animation
      $(".text").textillate(CONFIG.textillate);
      
      // Siri message animation
      $(".siri-message").textillate(CONFIG.siriMessage);
    } catch (error) {
      console.error('Error initializing text animations:', error);
    }
  },

  /**
   * Initialize Siri Wave visualization
   */
  initSiriWave() {
    try {
      const container = document.getElementById("siri-container");
      if (!container) {
        console.warn('Siri container not found');
        return;
      }

      State.siriWaveInstance = new SiriWave({
        container: container,
        ...CONFIG.siriWave
      });
      
      return State.siriWaveInstance;
    } catch (error) {
      console.error('Error initializing Siri Wave:', error);
    }
  }
};

/**
 * Voice Assistant Controller
 */
const VoiceAssistant = {
  /**
   * Activate voice input
   */
  async activate() {
    if (State.isProcessing) {
      console.log('Already processing a command');
      return;
    }

    State.isProcessing = true;

    try {
      // Play activation sound
      await Utils.callEel(eel.play_assistant_sound);
      
      // Show wave visualization
      Utils.toggleElement("#Oval", false);
      Utils.toggleElement("#SiriWave", true);
      
      // Take voice command
      await Utils.callEel(eel.takeAllCommands);
    } catch (error) {
      console.error('Error activating voice assistant:', error);
      Utils.showError('Failed to activate voice assistant');
    } finally {
      State.isProcessing = false;
    }
  },

  /**
   * Process text command
   */
  async processTextCommand(message) {
    if (!message || message.trim() === "") {
      console.log("Empty message, nothing sent.");
      return;
    }

    if (State.isProcessing) {
      console.log('Already processing a command');
      return;
    }

    State.isProcessing = true;

    try {
      // Hide oval, show wave
      Utils.toggleElement("#Oval", false);
      Utils.toggleElement("#SiriWave", true);
      
      // Send command to backend
      await Utils.callEel(eel.takeAllCommands, message);
      
      // Clear input
      $("#chatbox").val("");
      
      // Reset buttons
      this.updateButtons("");
    } catch (error) {
      console.error('Error processing text command:', error);
      Utils.showError('Failed to process command');
    } finally {
      State.isProcessing = false;
    }
  },

  /**
   * Update button visibility based on input
   */
  updateButtons(message) {
    const hasMicBtn = $("#MicBtn").length > 0;
    const hasSendBtn = $("#SendBtn").length > 0;

    if (message.length === 0) {
      if (hasMicBtn) $("#MicBtn").attr("hidden", false);
      if (hasSendBtn) $("#SendBtn").attr("hidden", true);
    } else {
      if (hasMicBtn) $("#MicBtn").attr("hidden", true);
      if (hasSendBtn) $("#SendBtn").attr("hidden", false);
    }
  }
};

/**
 * Chat Modal Controller
 */
const ChatModal = {
  /**
   * Open chat modal
   */
  open() {
    const modal = $("#ChatModal");
    if (modal.length) {
      modal.attr("hidden", false).addClass("fade-in");
      State.chatModalOpen = true;
      
      // Set focus to close button for accessibility
      $("#CloseChatBtn").focus();
    }
  },

  /**
   * Close chat modal
   */
  close() {
    const modal = $("#ChatModal");
    if (modal.length) {
      modal.addClass("fade-out");
      setTimeout(() => {
        modal.attr("hidden", true).removeClass("fade-in fade-out");
        State.chatModalOpen = false;
      }, 300);
    }
  },

  /**
   * Toggle chat modal
   */
  toggle() {
    if (State.chatModalOpen) {
      this.close();
    } else {
      this.open();
    }
  }
};

/**
 * Event Handlers
 */
const EventHandlers = {
  /**
   * Handle microphone button click
   */
  onMicClick(e) {
    e.preventDefault();
    VoiceAssistant.activate();
  },

  /**
   * Handle send button click
   */
  onSendClick(e) {
    e.preventDefault();
    const message = $("#chatbox").val();
    VoiceAssistant.processTextCommand(message);
  },

  /**
   * Handle chat button click
   */
  onChatClick(e) {
    e.preventDefault();
    ChatModal.toggle();
  },

  /**
   * Handle settings button click
   */
  onSettingsClick(e) {
    e.preventDefault();
    console.log('Settings clicked - implement settings panel');
    // TODO: Implement settings panel
  },

  /**
   * Handle chatbox input
   */
  onChatboxInput: Utils.debounce(function() {
    const message = $("#chatbox").val();
    VoiceAssistant.updateButtons(message);
  }, 100),

  /**
   * Handle chatbox key press
   */
  onChatboxKeyPress(e) {
    if (e.which === 13) { // Enter key
      e.preventDefault();
      const message = $("#chatbox").val();
      VoiceAssistant.processTextCommand(message);
    }
  },

  /**
   * Handle keyboard shortcuts
   */
  onKeyboardShortcut(e) {
    // Voice activation shortcut (Cmd+J or Ctrl+J)
    if (e.key === CONFIG.keyboard.voiceActivationKey && e.metaKey) {
      e.preventDefault();
      VoiceAssistant.activate();
    }

    // Close modal on Escape
    if (e.key === "Escape" && State.chatModalOpen) {
      e.preventDefault();
      ChatModal.close();
    }
  }
};

/**
 * Initialize application
 */
function initializeApp() {
  console.log('Initializing Jarvis Assistant...');

  // Initialize eel if available
  if (typeof eel !== 'undefined' && typeof eel.init === 'function') {
    try {
      eel.init()();
    } catch (error) {
      console.warn('Eel initialization failed:', error);
    }
  }

  // Initialize animations
  AnimationController.initTextAnimations();
  AnimationController.initSiriWave();

  // Attach event listeners
  $("#MicBtn").on("click", EventHandlers.onMicClick);
  $("#SendBtn").on("click", EventHandlers.onSendClick);
  $("#ChatBtn").on("click", EventHandlers.onChatClick);
  $("#SettingBtn").on("click", EventHandlers.onSettingsClick);
  $("#CloseChatBtn").on("click", () => ChatModal.close());
  
  $("#chatbox").on("input", EventHandlers.onChatboxInput);
  $("#chatbox").on("keypress", EventHandlers.onChatboxKeyPress);
  
  document.addEventListener("keydown", EventHandlers.onKeyboardShortcut, false);

  // Close chat modal when clicking outside
  $("#ChatModal").on("click", function(e) {
    if (e.target === this) {
      ChatModal.close();
    }
  });

  console.log('Jarvis Assistant initialized successfully');
}

/**
 * Document ready handler
 */
$(document).ready(function() {
  initializeApp();
});

/**
 * Error handling for unhandled promise rejections
 */
window.addEventListener('unhandledrejection', function(event) {
  console.error('Unhandled promise rejection:', event.reason);
  // Optionally notify user
  // Utils.showError('An unexpected error occurred');
});

/**
 * Export for testing/debugging
 */
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    VoiceAssistant,
    ChatModal,
    AnimationController,
    Utils,
    CONFIG,
    State
  };
}
