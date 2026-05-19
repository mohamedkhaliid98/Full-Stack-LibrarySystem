const API = "/api";

async function apiRequest(method, path, body = null) {
  const options = { method, credentials: "same-origin", headers: {} };
  if (body !== null) {
    options.headers["Content-Type"] = "application/json";
    options.body = JSON.stringify(body);
  }
  const response = await fetch(API + path, options);
  let data = {};
  try {
    data = await response.json();
  } catch {
    data = {};
  }
  if (!response.ok) {
    const error = new Error(data.error || response.statusText || "Request failed");
    error.status = response.status;
    error.data = data;
    throw error;
  }
  return data;
}
