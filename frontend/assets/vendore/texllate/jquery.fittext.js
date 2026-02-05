/**
 * FitText - Modern Vanilla JS Edition
 * Automatically adjusts font size to fit container width
 * 
 * @version 2.0.0
 * @author Modernized for 2025
 * @license MIT
 */

class FitText {
  constructor(selector, options = {}) {
    this.elements = typeof selector === 'string' 
      ? document.querySelectorAll(selector)
      : selector instanceof NodeList 
        ? selector 
        : [selector];
    
    this.settings = {
      compressor: options.compressor || 1,
      minFontSize: options.minFontSize || 0,
      maxFontSize: options.maxFontSize || Infinity,
      delay: options.delay || 100,
    };
    
    this.resizeTimeout = null;
    this.init();
  }
  
  init() {
    this.elements.forEach(element => {
      this.resize(element);
      
      // Use ResizeObserver for better performance
      if ('ResizeObserver' in window) {
        const observer = new ResizeObserver(() => {
          this.resize(element);
        });
        observer.observe(element);
      } else {
        // Fallback to window resize with debouncing
        window.addEventListener('resize', this.debounce(() => {
          this.resize(element);
        }, this.settings.delay));
      }
    });
  }
  
  resize(element) {
    const width = element.offsetWidth;
    const fontSize = Math.max(
      Math.min(
        width / (this.settings.compressor * 10),
        this.settings.maxFontSize
      ),
      this.settings.minFontSize
    );
    
    element.style.fontSize = `${fontSize}px`;
  }
  
  debounce(func, wait) {
    return (...args) => {
      clearTimeout(this.resizeTimeout);
      this.resizeTimeout = setTimeout(() => func.apply(this, args), wait);
    };
  }
}

// jQuery-style syntax support (optional)
if (typeof window !== 'undefined') {
  window.FitText = FitText;
  
  // Add as data attribute initializer
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-fittext]').forEach(element => {
      const compressor = parseFloat(element.dataset.fittext) || 1;
      const minSize = parseFloat(element.dataset.fittextMin) || 0;
      const maxSize = parseFloat(element.dataset.fittextMax) || Infinity;
      
      new FitText(element, {
        compressor,
        minFontSize: minSize,
        maxFontSize: maxSize,
      });
    });
  });
}

export default FitText;
