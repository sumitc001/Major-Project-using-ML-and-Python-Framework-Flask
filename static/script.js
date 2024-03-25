// // JavaScript for image slider
// const imageContainer = document.getElementById('image-container');
// const images = ['img/subham.jpg', 'img/bg1.jpg', 'img/bg2.jpg']; // Add your image paths here
// let currentIndex = 0;

// function changeImage() {
//     currentIndex = (currentIndex + 1) % images.length;
//     imageContainer.innerHTML = `<img src="${images[currentIndex]}" alt="Slide ${currentIndex + 1}">`;
// }

// setInterval(changeImage, 3000); // Change image every 3 seconds
// JavaScript for image slider
// JavaScript for image slider
const images = [
    '/static/bg3.jpg',
    '/static/bg.jpg',
    '/static/bg2.jpg',
    '/static/sk.jpg',
    '/static/sk1.jpg'
];

let currentIndex = 0;

// Function to change the image
const changeImage = () => {
    currentIndex = (currentIndex + 1) % images.length;
    document.getElementById('image-container').innerHTML = `<img src="${images[currentIndex]}" alt="Slide ${currentIndex + 1}">`;
};

// Start rotating images after the first image has loaded
document.addEventListener('DOMContentLoaded', () => {
    const img = new Image();
    img.onload = () => {
        document.getElementById('image-container').innerHTML = `<img src="${images[currentIndex]}" alt="Slide ${currentIndex + 1}">`;
        setInterval(changeImage, 3000); // Change image every 3 seconds
    };
    img.src = images[currentIndex];
});

