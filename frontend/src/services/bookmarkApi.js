import { apiFetch } from "../api";

export async function fetchBookmarks(searchQuery = "") {
  const url = searchQuery 
    ? `/api/bookmarks?query=${encodeURIComponent(searchQuery)}`
    : "/api/bookmarks";
  const response = await apiFetch(url);
  return response.bookmarks || [];
}

export async function createBookmark(bookmarkData) {
  const response = await apiFetch("/api/bookmarks", {
    method: "POST",
    body: JSON.stringify(bookmarkData),
  });
  return response;
}

export async function deleteBookmark(bookmarkId) {
  const response = await apiFetch(`/api/bookmarks/${bookmarkId}`, {
    method: "DELETE",
  });
  return response;
}

export async function toggleBookmarkFavorite(bookmarkId) {
  const response = await apiFetch(`/api/bookmarks/${bookmarkId}/favorite`, {
    method: "PATCH",
  });
  return response;
}
