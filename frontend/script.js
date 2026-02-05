/**
 * Particle Animation System for Jarvis Interface
 * Creates a 3D sphere particle effect with rotation and depth-based rendering
 */

// Configuration
const PARTICLE_CONFIG = {
  sphereRadius: 140,
  radiusScale: 1,
  particlesPerFrame: 8,
  particleLifespan: {
    attack: 50,
    hold: 50,
    decay: 100
  },
  particleRadius: 1.8,
  gravity: 0, // Positive for down, negative for up
  randomAccel: {
    x: 0.1,
    y: 0.1,
    z: 0.1
  },
  color: {
    r: 0,
    g: 72,
    b: 255
  },
  rotation: {
    speed: 2 * Math.PI / 1200 // One rotation every 1200 frames
  },
  camera: {
    focalLength: 320,
    zMax: 318,
    zeroAlphaDepth: -750
  },
  performance: {
    frameInterval: 10 / 24, // ~24 FPS
    maxParticles: 1000 // Limit for performance
  }
};

// Debug logger
const Debug = {
  enabled: false,
  log(message) {
    if (this.enabled) {
      try {
        console.log(message);
      } catch (exception) {
        return;
      }
    }
  }
};

/**
 * Particle System Manager
 */
class ParticleSystem {
  constructor(canvas, context) {
    this.canvas = canvas;
    this.context = context;
    this.displayWidth = canvas.width;
    this.displayHeight = canvas.height;
    
    // Particle storage
    this.particleList = { first: null };
    this.recycleBin = { first: null };
    this.particleCount = 0;
    
    // Animation state
    this.timer = null;
    this.frameCount = 0;
    this.turnAngle = 0;
    
    // Projection settings
    this.projCenterX = this.displayWidth / 2;
    this.projCenterY = this.displayHeight / 2;
    
    // Sphere position
    this.sphereCenterX = 0;
    this.sphereCenterY = 0;
    this.sphereCenterZ = -3 - PARTICLE_CONFIG.sphereRadius;
    
    // RGB string for performance
    this.rgbString = `rgba(${PARTICLE_CONFIG.color.r},${PARTICLE_CONFIG.color.g},${PARTICLE_CONFIG.color.b},`;
    
    this.init();
  }

  init() {
    Debug.log('Particle system initializing...');
    this.start();
  }

  start() {
    if (this.timer) {
      this.stop();
    }
    this.timer = setInterval(() => this.update(), PARTICLE_CONFIG.performance.frameInterval);
    Debug.log('Particle system started');
  }

  stop() {
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
      Debug.log('Particle system stopped');
    }
  }

  update() {
    this.frameCount++;
    
    // Add new particles
    if (this.particleCount < PARTICLE_CONFIG.performance.maxParticles) {
      this.spawnParticles();
    }
    
    // Update rotation
    this.turnAngle = (this.turnAngle + PARTICLE_CONFIG.rotation.speed) % (2 * Math.PI);
    const sinAngle = Math.sin(this.turnAngle);
    const cosAngle = Math.cos(this.turnAngle);
    
    // Clear canvas
    this.context.fillStyle = "#000000";
    this.context.fillRect(0, 0, this.displayWidth, this.displayHeight);
    
    // Update and render particles
    this.updateParticles(sinAngle, cosAngle);
  }

  spawnParticles() {
    for (let i = 0; i < PARTICLE_CONFIG.particlesPerFrame; i++) {
      // Generate random point on sphere surface
      const theta = Math.random() * 2 * Math.PI;
      const phi = Math.acos(Math.random() * 2 - 1);
      
      const x0 = PARTICLE_CONFIG.sphereRadius * Math.sin(phi) * Math.cos(theta);
      const y0 = PARTICLE_CONFIG.sphereRadius * Math.sin(phi) * Math.sin(theta);
      const z0 = PARTICLE_CONFIG.sphereRadius * Math.cos(phi);
      
      const particle = this.createParticle(
        x0,
        this.sphereCenterY + y0,
        this.sphereCenterZ + z0,
        0.002 * x0,
        0.002 * y0,
        0.002 * z0
      );
      
      if (particle) {
        // Set particle properties
        particle.attack = PARTICLE_CONFIG.particleLifespan.attack;
        particle.hold = PARTICLE_CONFIG.particleLifespan.hold;
        particle.decay = PARTICLE_CONFIG.particleLifespan.decay;
        particle.initValue = 0;
        particle.holdValue = 1;
        particle.lastValue = 0;
        particle.stuckTime = 90 + Math.random() * 20;
        particle.accelX = 0;
        particle.accelY = PARTICLE_CONFIG.gravity;
        particle.accelZ = 0;
      }
    }
  }

  createParticle(x0, y0, z0, vx0, vy0, vz0) {
    let particle;
    
    // Try to recycle a particle
    if (this.recycleBin.first !== null) {
      particle = this.recycleBin.first;
      
      // Remove from recycle bin
      if (particle.next !== null) {
        this.recycleBin.first = particle.next;
        particle.next.prev = null;
      } else {
        this.recycleBin.first = null;
      }
    } else {
      // Create new particle
      particle = {};
      this.particleCount++;
    }
    
    // Add to particle list
    if (this.particleList.first === null) {
      this.particleList.first = particle;
      particle.prev = null;
      particle.next = null;
    } else {
      particle.next = this.particleList.first;
      this.particleList.first.prev = particle;
      this.particleList.first = particle;
      particle.prev = null;
    }
    
    // Initialize particle
    particle.x = x0;
    particle.y = y0;
    particle.z = z0;
    particle.velX = vx0;
    particle.velY = vy0;
    particle.velZ = vz0;
    particle.age = 0;
    particle.dead = false;
    
    return particle;
  }

  updateParticles(sinAngle, cosAngle) {
    let p = this.particleList.first;
    
    while (p !== null) {
      const nextParticle = p.next;
      
      // Update age
      p.age++;
      
      // Move particle if past stuck time
      if (p.age > p.stuckTime) {
        p.velX += p.accelX + PARTICLE_CONFIG.randomAccel.x * (Math.random() * 2 - 1);
        p.velY += p.accelY + PARTICLE_CONFIG.randomAccel.y * (Math.random() * 2 - 1);
        p.velZ += p.accelZ + PARTICLE_CONFIG.randomAccel.z * (Math.random() * 2 - 1);
        
        p.x += p.velX;
        p.y += p.velY;
        p.z += p.velZ;
      }
      
      // Calculate rotated and projected coordinates
      const rotX = cosAngle * p.x + sinAngle * (p.z - this.sphereCenterZ);
      const rotZ = -sinAngle * p.x + cosAngle * (p.z - this.sphereCenterZ) + this.sphereCenterZ;
      const m = PARTICLE_CONFIG.radiusScale * PARTICLE_CONFIG.camera.focalLength / 
                (PARTICLE_CONFIG.camera.focalLength - rotZ);
      
      p.projX = rotX * m + this.projCenterX;
      p.projY = p.y * m + this.projCenterY;
      
      // Update alpha based on age
      this.updateParticleAlpha(p);
      
      // Check if particle is in view
      const outsideView = (
        p.projX > this.displayWidth ||
        p.projX < 0 ||
        p.projY < 0 ||
        p.projY > this.displayHeight ||
        rotZ > PARTICLE_CONFIG.camera.zMax
      );
      
      if (outsideView || p.dead) {
        this.recycleParticle(p);
      } else {
        // Render particle
        this.renderParticle(p, rotZ, m);
      }
      
      p = nextParticle;
    }
  }

  updateParticleAlpha(p) {
    const totalLifespan = p.attack + p.hold + p.decay;
    
    if (p.age < totalLifespan) {
      if (p.age < p.attack) {
        p.alpha = (p.holdValue - p.initValue) / p.attack * p.age + p.initValue;
      } else if (p.age < p.attack + p.hold) {
        p.alpha = p.holdValue;
      } else {
        const decayProgress = p.age - p.attack - p.hold;
        p.alpha = (p.lastValue - p.holdValue) / p.decay * decayProgress + p.holdValue;
      }
    } else {
      p.dead = true;
    }
  }

  renderParticle(p, rotZ, m) {
    // Calculate depth-based alpha
    let depthAlphaFactor = 1 - rotZ / PARTICLE_CONFIG.camera.zeroAlphaDepth;
    depthAlphaFactor = Math.max(0, Math.min(1, depthAlphaFactor));
    
    // Set fill style
    this.context.fillStyle = this.rgbString + (depthAlphaFactor * p.alpha) + ")";
    
    // Draw particle
    this.context.beginPath();
    this.context.arc(
      p.projX,
      p.projY,
      m * PARTICLE_CONFIG.particleRadius,
      0,
      2 * Math.PI,
      false
    );
    this.context.closePath();
    this.context.fill();
  }

  recycleParticle(p) {
    // Remove from particle list
    if (this.particleList.first === p) {
      if (p.next !== null) {
        p.next.prev = null;
        this.particleList.first = p.next;
      } else {
        this.particleList.first = null;
      }
    } else {
      if (p.next === null) {
        p.prev.next = null;
      } else {
        p.prev.next = p.next;
        p.next.prev = p.prev;
      }
    }
    
    // Add to recycle bin
    if (this.recycleBin.first === null) {
      this.recycleBin.first = p;
      p.prev = null;
      p.next = null;
    } else {
      p.next = this.recycleBin.first;
      this.recycleBin.first.prev = p;
      this.recycleBin.first = p;
      p.prev = null;
    }
  }

  updateSphereRadius(radius) {
    PARTICLE_CONFIG.sphereRadius = radius;
    this.sphereCenterZ = -3 - radius;
    Debug.log(`Sphere radius updated to ${radius}`);
  }

  updateRadiusScale(scale) {
    PARTICLE_CONFIG.radiusScale = scale;
    Debug.log(`Radius scale updated to ${scale}`);
  }
}

/**
 * Initialize particle system when window loads
 */
let particleSystem = null;

window.addEventListener("load", () => {
  Debug.log('Window loaded, initializing particle system...');
  
  // Check for canvas support
  if (!Modernizr.canvas) {
    console.error('Canvas not supported');
    return;
  }
  
  const canvas = document.getElementById("canvasOne");
  if (!canvas) {
    console.error('Canvas element not found');
    return;
  }
  
  const context = canvas.getContext("2d");
  if (!context) {
    console.error('Could not get 2D context');
    return;
  }
  
  // Create particle system
  particleSystem = new ParticleSystem(canvas, context);
  
  Debug.log('Particle system initialized successfully');
}, false);

/**
 * jQuery UI Sliders for controlling particle system (if needed)
 */
$(function() {
  // Sphere radius slider
  const radiusSlider = $("#slider-range");
  if (radiusSlider.length) {
    radiusSlider.slider({
      range: false,
      min: 20,
      max: 500,
      value: 280,
      slide: function(event, ui) {
        if (particleSystem) {
          particleSystem.updateSphereRadius(ui.value);
        }
      }
    });
  }
  
  // Radius scale slider
  const scaleSlider = $("#slider-test");
  if (scaleSlider.length) {
    scaleSlider.slider({
      range: false,
      min: 1.0,
      max: 2.0,
      value: 1,
      step: 0.01,
      slide: function(event, ui) {
        if (particleSystem) {
          particleSystem.updateRadiusScale(ui.value);
        }
      }
    });
  }
});

/**
 * Cleanup on page unload
 */
window.addEventListener("beforeunload", () => {
  if (particleSystem) {
    particleSystem.stop();
    Debug.log('Particle system stopped');
  }
});

/**
 * Export for testing/debugging
 */
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    ParticleSystem,
    PARTICLE_CONFIG,
    Debug
  };
}
