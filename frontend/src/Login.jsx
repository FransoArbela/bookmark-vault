import { useState } from "react";
import { loginUser, registerUser } from "./services/authApi";

export default function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isRegister, setIsRegister] = useState(false);

  async function handleLogin(event) {
    event.preventDefault();
    setError("");

    const response = await loginUser(username, password);

    if (response.error) {
      setError(response.error);
      return;
    }

    setTimeout(() => {
      onLogin();
    }, 100);
  }

  async function handleRegister(event) {
    event.preventDefault();
    setError("");

    const response = await registerUser(username, password);

    if (response.error) {
      setError(response.error);
      return;
    }

    setTimeout(() => {
      handleLogin(event);
    }, 100);
  }

  const handleSubmit = isRegister ? handleRegister : handleLogin;

  return (
    <form onSubmit={handleSubmit} className="form-card">
      <h2 className="header-secondary">
        {isRegister ? "Create Account" : "Sign In"}
      </h2>

      <div className="space-y-4">
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(event) => setUsername(event.target.value)}
          className="form-input"
          required
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          className="form-input"
          required
        />
      </div>

      <button type="submit" className="btn-primary w-full">
        {isRegister ? "Create Account" : "Sign In"}
      </button>

      <button
        type="button"
        onClick={() => setIsRegister(!isRegister)}
        className="w-full text-primary-600 hover:text-primary-500 text-sm font-medium"
      >
        {isRegister ? "Already have an account? Sign in" : "Don't have an account? Sign up"}
      </button>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded text-sm">
          {error}
        </div>
      )}
    </form>
  );
}
