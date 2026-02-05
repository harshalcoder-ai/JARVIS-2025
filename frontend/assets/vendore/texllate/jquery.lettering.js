/**
 * Lettering - Modern Vanilla JS Edition
 * Splits text into individual letters, words, or lines wrapped in spans
 * 
 * @version 2.0.0
 * @author Modernized for 2025
 * @license MIT
 */

class Lettering {
  constructor(selector, options = {}) {
    this.elements = typeof selector === 'string' 
      ? document.querySelectorAll(selector)
      : selector instanceof NodeList 
        ? selector 
        : [selector];
    
    this.settings = {
      type: options.type || 'letters', // 'letters', 'words', or 'lines'
      classPrefix: options.classPrefix || '',
      tag: options.tag || 'span',
    };
    
    this.init();
  }
  
  init() {
    this.elements.forEach(element => {
      switch(this.settings.type) {
        case 'words':
          this.splitWords(element);
          break;
        case 'lines':
          this.splitLines(element);
          break;
        default:
          this.splitLetters(element);
      }
    });
  }
  
  splitLetters(element) {
    const text = element.textContent;
    const letters = text.split('');
    
    element.innerHTML = letters
      .map((letter, index) => {
        const className = this.settings.classPrefix 
          ? `${this.settings.classPrefix}char${index + 1}` 
          : `char${index + 1}`;
        return letter === ' ' 
          ? ' ' 
          : `<${this.settings.tag} class="${className}" aria-hidden="true">${letter}</${this.settings.tag}>`;
      })
      .join('');
    
    // Preserve original text for screen readers
    element.setAttribute('aria-label', text);
  }
  
  splitWords(element) {
    const text = element.textContent;
    const words = text.split(/\s+/);
    
    element.innerHTML = words
      .map((word, index) => {
        const className = this.settings.classPrefix 
          ? `${this.settings.classPrefix}word${index + 1}` 
          : `word${index + 1}`;
        return `<${this.settings.tag} class="${className}" aria-hidden="true">${word}</${this.settings.tag}>`;
      })
      .join(' ');
    
    element.setAttribute('aria-label', text);
  }
  
  splitLines(element) {
    // Store original HTML to preserve <br> tags
    const html = element.innerHTML;
    const lines = html.split(/<br\s*\/?>/i);
    
    element.innerHTML = lines
      .map((line, index) => {
        const className = this.settings.classPrefix 
          ? `${this.settings.classPrefix}line${index + 1}` 
          : `line${index + 1}`;
        return line.trim() 
          ? `<${this.settings.tag} class="${className}" aria-hidden="true">${line}</${this.settings.tag}>` 
          : '';
      })
      .filter(Boolean)
      .join('');
    
    element.setAttribute('aria-label', element.textContent);
  }
  
  // Static method for quick use
  static apply(selector, type = 'letters', options = {}) {
    return new Lettering(selector, { ...options, type });
  }
}

// Expose globally
if (typeof window !== 'undefined') {
  window.Lettering = Lettering;
  
  // Auto-initialize elements with data attributes
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-lettering]').forEach(element => {
      const type = element.dataset.lettering || 'letters';
      const prefix = element.dataset.letteringPrefix || '';
      
      new Lettering(element, { 
        type, 
        classPrefix: prefix 
      });
    });
  });
}

export default Lettering;
