import logo from './logo.svg';
import './App.css';
import HandTracking from './components/HandTracking';


function App() {
  return (
    <div className="App">
      <header className="App-header">
        {/* Your existing logo and text */}
        <img src={logo} className="App-logo" alt="logo" />
        <p>Edit <code>src/App.js</code> and save to reload.</p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>

        {/* Add your HandTracking component here */}
        <HandTracking />
      </header>
    </div>
  );
}


export default App;
