/**
 * Portfolio App Logic
 */

import PhotoSwipeLightbox from 'https://unpkg.com/photoswipe@5.4.2/dist/photoswipe-lightbox.esm.js';
import PhotoSwipe from 'https://unpkg.com/photoswipe@5.4.2/dist/photoswipe.esm.js';

document.addEventListener('DOMContentLoaded', () => {
    // Mobile Menu Toggle
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');
    
    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });
    }

    // Initialize PhotoSwipe if gallery exists
    const gallery = document.getElementById('gallery');
    if (gallery) {
        const lightbox = new PhotoSwipeLightbox({
            gallery: '#gallery',
            children: 'a',
            pswpModule: PhotoSwipe
        });
        lightbox.init();
    }

    // Asset Protection: Prevent Right-Click and Dragging
    document.addEventListener('contextmenu', event => {
        event.preventDefault();
    });

    document.addEventListener('dragstart', event => {
        event.preventDefault();
    });
});




