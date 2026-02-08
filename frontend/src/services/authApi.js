import { apiFetch } from "../api";

export async function registerUser(username, password) {
  const response = await apiFetch("/api/register", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
  return response;
}

export async function loginUser(username, password) {
  const response = await apiFetch("/api/login", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
  return response;
}

export async function logoutUser() {
  const response = await apiFetch("/api/logout", {
    method: "POST",
  });
  return response;
}

export async function fetchCurrentUser() {
  const response = await apiFetch("/api/me");
  return response.user;
}
