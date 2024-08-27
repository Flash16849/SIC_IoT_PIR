// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getDatabase, ref, get } from "firebase/database"; // Dành cho Realtime Database
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDGLclDfxL5X6Apu6MiP2YS7h_nThxJLjg",
  authDomain: "sic-iot-ab9de.firebaseapp.com",
  databaseURL: "https://sic-iot-ab9de-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "sic-iot-ab9de",
  storageBucket: "sic-iot-ab9de.appspot.com",
  messagingSenderId: "680804567994",
  appId: "1:680804567994:web:03622cc8fa4e170bf8ab83",
  measurementId: "G-GMQY17FC9R"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

// export const database = firebase.database();
// Thiết lập Realtime Database
const database = getDatabase(app);

export { database };