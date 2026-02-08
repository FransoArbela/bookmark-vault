import { useEffect, useState } from "react";
import { fetchBookmarks, createBookmark, deleteBookmark, toggleBookmarkFavorite } from "./services/bookmarkApi";

export default function Bookmarks() {
  const [bookmarks, setBookmarks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  
  // Form state
  const [title, setTitle] = useState("");
  const [url, setUrl] = useState("");
  const [tags, setTags] = useState("");
  const [note, setNote] = useState("");
  const [formError, setFormError] = useState("");
  const [formLoading, setFormLoading] = useState(false);

  async function loadBookmarks(query = "") {
    setLoading(true);
    const bookmarksData = await fetchBookmarks(query);
    setBookmarks(bookmarksData);
    setLoading(false);
  }

  useEffect(() => {
    let cancelled = false;

    async function fetchInitialBookmarks() {
      setLoading(true);
      const bookmarksData = await fetchBookmarks();
      if (cancelled) return;
      setBookmarks(bookmarksData);
      setLoading(false);
    }

    fetchInitialBookmarks();

    return () => {
      cancelled = true;
    };
  }, []);

  async function handleCreateBookmark(event) {
    event.preventDefault();
    setFormError("");
    setFormLoading(true);

    const response = await createBookmark({
      title: title.trim(),
      url: url.trim(),
      tags: tags.trim(),
      note: note.trim(),
    });

    setFormLoading(false);

    if (response.error) {
      setFormError(response.error);
      return;
    }

    setTitle("");
    setUrl("");
    setTags("");
    setNote("");
    loadBookmarks(searchQuery);
  }

  function handleSearch(event) {
    event.preventDefault();
    loadBookmarks(searchQuery.trim());
  }

  async function handleDeleteBookmark(id) {
    if (!window.confirm("Delete this bookmark?")) {
      return;
    }

    const response = await deleteBookmark(id);

    if (response.error) {
      alert("Error deleting bookmark: " + response.error);
      return;
    }

    setBookmarks(bookmarks.filter((bookmark) => bookmark.id !== id));
  }

  async function handleToggleFavorite(id) {
    const response = await toggleBookmarkFavorite(id);

    if (response.error) {
      alert("Error updating favorite: " + response.error);
      return;
    }

    setBookmarks(
      bookmarks.map((bookmark) =>
        bookmark.id === id ? { ...bookmark, is_favorite: response.is_favorite } : bookmark
      )
    );
  }

  return (
    <div className="space-y-8">
      {/* Create Bookmark Form */}
      <div className="form-section">
        <h2 className="header-secondary">Add New Bookmark</h2>
        <form onSubmit={handleCreateBookmark} className="space-y-4">
          <div>
            <input
              type="text"
              placeholder="Bookmark title"
              value={title}
              onChange={(event) => setTitle(event.target.value)}
              className="form-input"
              required
            />
          </div>

          <div>
            <input
              type="url"
              placeholder="URL (https://example.com)"
              value={url}
              onChange={(event) => setUrl(event.target.value)}
              className="form-input"
              required
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <input
              type="text"
              placeholder="Tags (optional)"
              value={tags}
              onChange={(event) => setTags(event.target.value)}
              className="form-input"
            />
            <input
              type="text"
              placeholder="Category (optional)"
              value={note}
              onChange={(event) => setNote(event.target.value)}
              className="form-input"
            />
          </div>

          <button type="submit" className="btn-primary w-full" disabled={formLoading}>
            {formLoading ? "Adding..." : "Add Bookmark"}
          </button>

          {formError && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded text-sm">
              {formError}
            </div>
          )}
        </form>
      </div>

      {/* Search Section */}
      <div className="search-section">
        <form onSubmit={handleSearch} className="flex gap-2">
          <input
            type="text"
            placeholder="Search bookmarks by title, tags, or URL..."
            value={searchQuery}
            onChange={(event) => setSearchQuery(event.target.value)}
            className="form-input flex-1"
          />
          <button type="submit" className="btn-primary">
            Search
          </button>
        </form>
      </div>

      {/* Bookmarks List */}
      <div>
        {loading && (
          <div className="text-center py-8">
            <p className="text-gray-600">Loading bookmarks...</p>
          </div>
        )}

        {!loading && bookmarks.length === 0 && (
          <div className="text-center py-12 bg-white rounded border border-gray-200 shadow-sm p-8">
            <p className="text-gray-600 mb-2">No bookmarks yet.</p>
            <p className="text-gray-400 text-sm">Start by adding your first bookmark above.</p>
          </div>
        )}

        {!loading && bookmarks.length > 0 && (
          <div className="grid gap-4">
            {bookmarks.map((bookmark) => (
              <div
                key={bookmark.id}
                className={`card ${
                  bookmark.is_favorite
                    ? "card-favorite hover:shadow-md"
                    : "hover:border-primary-300"
                }`}
              >
                <div className="flex justify-between items-start gap-4 mb-3">
                  <div className="flex-1 min-w-0">
                    <a
                      href={bookmark.url}
                      target="_blank"
                      rel="noreferrer"
                      className="link-primary-bold"
                    >
                      {Boolean(bookmark.is_favorite) && <span className="text-accent-500 text-xl">★</span>}
                      {bookmark.title}
                    </a>
                    <p className="bookmark-url">
                      {bookmark.url}
                    </p>
                  </div>
                </div>

                {bookmark.tags && (
                  <div className="mb-2 flex flex-wrap gap-1">
                    {bookmark.tags.split(",").map((tag, index) => (
                      <span
                        key={index}
                        className="tag"
                      >
                        {tag.trim()}
                      </span>
                    ))}
                  </div>
                )}

                {bookmark.note && (
                  <p className="bookmark-note">
                    "{bookmark.note}"
                  </p>
                )}

                <div className="flex-between pt-3 border-t border-gray-100">
                  <p className="bookmark-meta">
                    Added {new Date(bookmark.created_at).toLocaleDateString()}
                  </p>
                  <div className="flex gap-2">
                    <button
                      onClick={() => handleToggleFavorite(bookmark.id)}
                      className="btn-favorite"
                      title={bookmark.is_favorite ? "Remove from favorites" : "Add to favorites"}
                    >
                      {bookmark.is_favorite ? "★" : "☆"}
                    </button>

                    <button
                      onClick={() => handleDeleteBookmark(bookmark.id)}
                      className="btn-danger"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
