import './home.css';

function Home() {
  return (
    <div className="container">
        <div class="home">
            <div class="home-box">
                <h1>You have been scanned!</h1>
                <p>By our state of the art Space radar array.</p>
                <button class="gotologin-button" onClick={handleGOClick}>Take a look.</button>
            </div>
        </div>
    </div>
  );
}

export default Home;
