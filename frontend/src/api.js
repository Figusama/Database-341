const request = async (method, path, body) => {
    const res = await fetch(path, {
        method, 
        headers: {'Content-type': 'application/json'},
        body: body ? JSON.stringify(body) : undefined,
    })

    if(res.status === 204) return null
    const data = await res.json().catch(() => null)

    if(!res.ok) throw new Error(typeof data?.detail === "string" ? data.detail : JSON.stringify(data?.detail))
    
    return data
}


const crud = (base) => ({
    list: () => request("GET", base),
    get: (id) => request("GET", `${base}/${id}`),
    create: (body) => request("POST", base, body),
    update: (id, body) => request("PATCH", `${base}/${id}`, body),
    remove: (id) => request("DELETE", `${base}/${id}`),
})

export const api = {
  conferences: () => request("GET", "/conferences"),
  tracks: () => request("GET", "/tracks"),
  authors: () => request("GET", "/authors"),
  reviewers: () => request("GET", "/reviewers"),
  users: crud("/users"),
  papers: {
    ...crud("/papers"),
    addVersion: (id, version) => request("POST", `/papers/${id}/versions`, version),
    deleteVersion: (id, versionNo) => request("DELETE", `/papers/${id}/versions/${versionNo}`),
    setSession: (id, sessionId) => request("PATCH", `/papers/${id}`, { session_id: sessionId }),
  },
  reviews: {
    ...crud("/reviews"),
    update: (id, body) => request("PUT", `/reviews/${id}`, body),
  },
  sessions: crud("/sessions"),
}
