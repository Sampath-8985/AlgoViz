// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyAzhvUGqF7KK2DDZjx8D67EVr1T7vUhVHc",
    authDomain: "algoviz-4479f.firebaseapp.com",
    projectId: "algoviz-4479f",
    storageBucket: "algoviz-4479f.firebasestorage.app",
    messagingSenderId: "1026782510040",
    appId: "1:1026782510040:web:4ed369c1f2693944fc10ad"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

console.log("Firebase initialized:", app);
