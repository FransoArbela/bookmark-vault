import { useEffect, useState } from "react";
import { fetchCurrentUser, logoutUser } from "./services/authApi";
import Login from "./Login";
import Bookmarks from "./Bookmarks";

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  async function loadUser() {
    const currentUser = await fetchCurrentUser();
    setUser(currentUser);
    setLoading(false);
  }

  useEffect(() => {
    let cancelled = false;
    async function fetchUser() {
      const currentUser = await fetchCurrentUser();
      if (cancelled) return;
      setUser(currentUser);
      setLoading(false);
    }
    fetchUser();
    return () => {
      cancelled = true;
    };
  }, []);

  async function logout() {
    await logoutUser();
    setUser(null);
  }

  if (loading)
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <p className="text-gray-600">Loading...</p>
      </div>
    );

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center gradient-primary-accent px-4">
        <div className="w-full max-w-md">
          <h1 className="header-primary mb-2 text-center">
            Bookmark Vault
          </h1>
          <p className="text-gray-600 text-center mb-8">Save and organize your favorite links</p>
          <Login onLogin={loadUser} />
        </div>
      </div>
    );
  }

  return (
      <div className="min-h-screen bg-linear-to-br from-gray-50 to-accent-50">
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-4xl mx-auto px-4 py-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="header-primary">Bookmark Vault</h1>
              <p className="subheader">
                Welcome, <span className="font-semibold text-primary-600">{user.username}</span>
              </p>
            </div>
            <button onClick={logout} className="btn-primary">
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8">
        <Bookmarks />
      </main>
    </div>
  );
}

export default App;
