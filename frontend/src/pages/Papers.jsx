import { useEffect, useState } from "react"
import { api } from "../api"

const STATUSES = ["submitted", "under review", "accepted", "rejected", "withdrawn"]

const today = () => new Date().toISOString().slice(0, 10)
const now = () => {
    const date = new Date()
    date.setMinutes(date.getMinutes() - date.getTimezoneOffset())
    return date.toISOString().slice(0, 16)
}

const EMPTY_FORM = {
    track_id: "",
    title: "",
    abstract: "",
    submission_date: today(),
    status: "submitted",
    keywords: "",            
    authors: [""],          
    corresponding: 0,       

    file_location: "",
    uploaded_at: now(),
    change_note: "",
}

const EMPTY_VERSION = { version_no: "", file_location: "", uploaded_at: now(), change_note: "" }


const toList = (text) => {
    const items = text
        .split(",")
        .map((item) => item.trim())
        .filter((item) => item !== "")
    return [...new Set(items)]
}


const Papers = () => {
    const [papers, setPapers] = useState([])
    const [tracks, setTracks] = useState([])
    const [authors, setAuthors] = useState([])
    const [sessions, setSessions] = useState([])

    const [form, setForm] = useState(EMPTY_FORM)
    const [editingId, setEditingId] = useState(null)

    const [versions, setVersions] = useState([])
    const [newVersion, setNewVersion] = useState(EMPTY_VERSION)
    const [sessionId, setSessionId] = useState("")

    const [error, setError] = useState("")
    const [message, setMessage] = useState("")

    const load = () => {
        api.papers.list()
            .then((data) => setPapers(data))
            .catch((error) => setError(error.message))
    }

    useEffect(() => {
        load()
        api.tracks()
            .then((data) => setTracks(data))
            .catch((error) => setError(error.message))
        api.authors()
            .then((data) => setAuthors(data))
            .catch((error) => setError(error.message))
        api.sessions.list()
            .then((data) => setSessions(data))
            .catch((error) => setError(error.message))
    }, [])

    const set = (field) => {
        return (event) => {
            setForm({ ...form, [field]: event.target.value })
        }
    }

    const setVersionField = (field) => {
        return (event) => {
            setNewVersion({ ...newVersion, [field]: event.target.value })
        }
    }

    const clearMessages = () => {
        setError("")
        setMessage("")
    }

    const changeAuthor = (index, authorId) => {
        const updated = [...form.authors]
        updated[index] = authorId
        setForm({ ...form, authors: updated })
    }

    const addAuthor = () => {
        setForm({ ...form, authors: [...form.authors, ""] })
    }

    const removeAuthor = (index) => {
        const updated = form.authors.filter((_, i) => i !== index)
        let corresponding = form.corresponding
        if (index === corresponding) corresponding = 0
        else if (index < corresponding) corresponding = corresponding - 1
        setForm({ ...form, authors: updated, corresponding: corresponding })
    }

    const moveAuthor = (index, direction) => {
        const target = index + direction
        if (target < 0 || target >= form.authors.length) return
        const updated = [...form.authors]
        const temp = updated[index]
        updated[index] = updated[target]
        updated[target] = temp
        let corresponding = form.corresponding
        if (corresponding === index) corresponding = target
        else if (corresponding === target) corresponding = index
        setForm({ ...form, authors: updated, corresponding: corresponding })
    }

    const reset = () => {
        setForm({ ...EMPTY_FORM, submission_date: today(), uploaded_at: now() })
        setEditingId(null)
        setVersions([])
        setNewVersion(EMPTY_VERSION)
        setSessionId("")
    }

    const save = async (event) => {
        event.preventDefault()
        clearMessages()

        if (form.authors.some((id) => id === "")) {
            setError("Choose an author in every row or remove empty rows")
            return
        }
        if (new Set(form.authors).size !== form.authors.length) {
            setError("The same author is listed twice")
            return
        }
        if (toList(form.keywords).length === 0) {
            setError("Add at least one keyword")
            return
        }

        const body = {
            track_id: form.track_id,
            title: form.title,
            abstract: form.abstract,
            submission_date: form.submission_date,
            status: form.status,
            keywords: toList(form.keywords),
            authors: form.authors.map((authorId, index) => ({
                author_id: authorId,
                author_position: index + 1,
                is_corresponding: index === form.corresponding,
            })),
        }

        try {
            if (editingId) {
                await api.papers.update(editingId, body)
                setMessage("Paper updated")
            } else {
                body.versions = [{
                    version_no: 1,
                    file_location: form.file_location,
                    uploaded_at: form.uploaded_at,
                    change_note: form.change_note || null,
                }]
                await api.papers.create(body)
                setMessage("Paper created")
            }
            reset()
            load()
        } catch (error) {
            setError(error.message)
        }
    }


    const edit = async (id) => {
        clearMessages()
        try {
            const paper = await api.papers.get(id)
            const sortedAuthors = [...paper.authors].sort((a, b) => a.author_position - b.author_position)

            setForm({
                ...EMPTY_FORM,
                track_id: paper.track_id,
                title: paper.title,
                abstract: paper.abstract,
                submission_date: paper.submission_date,
                status: paper.status,
                keywords: paper.keywords.join(", "),
                authors: sortedAuthors.map((a) => a.author_id),
                corresponding: sortedAuthors.findIndex((a) => a.is_corresponding),
            })
            setVersions(paper.versions)
            setSessionId(paper.session_id ?? "")
            setEditingId(id)
        } catch (error) {
            setError(error.message)
        }
    }

    const remove = async (id) => {
        if (!confirm("Delete this paper? Its authors list, keywords, versions and reviews will be deleted too.")) return
        clearMessages()
        try {
            await api.papers.remove(id)
            setMessage("Paper deleted")
            if (id === editingId) reset()
            load()
        } catch (error) {
            setError(error.message)
        }
    }




    const reloadVersions = async () => {
        const paper = await api.papers.get(editingId)
        setVersions(paper.versions)
    }

    const addVersion = async (event) => {
        event.preventDefault()
        clearMessages()
        try {
            await api.papers.addVersion(editingId, {
                version_no: Number(newVersion.version_no),
                file_location: newVersion.file_location,
                uploaded_at: newVersion.uploaded_at,
                change_note: newVersion.change_note || null,
            })
            setMessage("Version added")
            setNewVersion(EMPTY_VERSION)
            await reloadVersions()
        } catch (error) {
            setError(error.message)
        }
    }

    const deleteVersion = async (versionNo) => {
        if (!confirm(`Delete version ${versionNo}?`)) return
        clearMessages()
        try {
            await api.papers.deleteVersion(editingId, versionNo)
            setMessage("Version deleted")
            await reloadVersions()
        } catch (error) {
            setError(error.message)
        }
    }





    const assignSession = async () => {
        clearMessages()
        try {
            await api.papers.setSession(editingId, sessionId || null)
            setMessage(sessionId ? "Paper assigned to session" : "Paper removed from session")
            load()
        } catch (error) {
            setError(error.message)   
        }
    }

    const sessionTitle = (id) => {
        const session = sessions.find((s) => s.session_id === id)
        return session ? session.title : ""
    }


    return (
        <>
            <h2>Papers</h2>

            {error && <div className="error">Error: {error}</div>}
            {message && <div className="ok">{message}</div>}

            <form className="box" onSubmit={save}>
                <h3>{editingId ? "Edit paper" : "Create paper"}</h3>

                <label>
                    Track
                    <select value={form.track_id} onChange={set("track_id")} required>
                        <option value="">-- choose --</option>
                        {tracks.map((track) => (
                            <option key={track.track_id} value={track.track_id}>
                                {track.name}
                            </option>
                        ))}
                    </select>
                </label>

                <label>
                    Title
                    <input value={form.title} onChange={set("title")} required />
                </label>

                <label>
                    Abstract
                    <textarea value={form.abstract} onChange={set("abstract")} required />
                </label>

                <label>
                    Submission date
                    <input type="date" value={form.submission_date} onChange={set("submission_date")} required />
                </label>

                <label>
                    Status
                    <select value={form.status} onChange={set("status")}>
                        {STATUSES.map((status) => (
                            <option key={status} value={status}>{status}</option>
                        ))}
                    </select>
                </label>

                <label>
                    Keywords (comma separated)
                    <input value={form.keywords} onChange={set("keywords")} required />
                </label>

                <div className="box">
                    <h4>Authors (order = author position)</h4>
                    <table>
                        <thead>
                            <tr>
                                <th>Position</th>
                                <th>Author</th>
                                <th>Corresponding</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {form.authors.map((authorId, index) => (
                                <tr key={index}>
                                    <td>{index + 1}</td>
                                    <td>
                                        <select value={authorId} onChange={(event) => changeAuthor(index, event.target.value)}>
                                            <option value="">-- choose --</option>
                                            {authors.map((author) => (
                                                <option key={author.author_id} value={author.author_id}>
                                                    {author.given_name} {author.surname}
                                                </option>
                                            ))}
                                        </select>
                                    </td>
                                    <td>
                                        <input
                                            type="radio"
                                            name="corresponding"
                                            checked={form.corresponding === index}
                                            onChange={() => setForm({ ...form, corresponding: index })}
                                        />
                                    </td>
                                    <td>
                                        <button type="button" onClick={() => moveAuthor(index, -1)}>Up</button>
                                        <button type="button" onClick={() => moveAuthor(index, 1)}>Down</button>
                                        {form.authors.length > 1 && (
                                            <button type="button" onClick={() => removeAuthor(index)}>Remove</button>
                                        )}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                    <button type="button" onClick={addAuthor}>+ Add author</button>
                </div>

                {!editingId && (
                    <div className="box">
                        <h4>First version</h4>
                        <label>
                            File location
                            <input
                                value={form.file_location}
                                onChange={set("file_location")}
                                placeholder="papers/new/v1.pdf"
                                required
                            />
                        </label>
                        <label>
                            Uploaded at
                            <input type="datetime-local" value={form.uploaded_at} onChange={set("uploaded_at")} required />
                        </label>
                        <label>
                            Change note (optional)
                            <input value={form.change_note} onChange={set("change_note")} />
                        </label>
                    </div>
                )}

                <button type="submit">{editingId ? "Save changes" : "Create paper"}</button>
                {editingId && (
                    <button type="button" onClick={reset}>
                        Cancel edit
                    </button>
                )}
            </form>

            {editingId && (
                <>
                    <div className="box">
                        <h3>Versions</h3>
                        <table>
                            <thead>
                                <tr>
                                    <th>No</th>
                                    <th>File location</th>
                                    <th>Uploaded at</th>
                                    <th>Change note</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {versions.map((version) => (
                                    <tr key={version.version_no}>
                                        <td>{version.version_no}</td>
                                        <td>{version.file_location}</td>
                                        <td>{version.uploaded_at}</td>
                                        <td>{version.change_note}</td>
                                        <td>
                                            <button onClick={() => deleteVersion(version.version_no)}>Delete</button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>

                        <form onSubmit={addVersion}>
                            <h4>Add version</h4>
                            <label>
                                File location
                                <input value={newVersion.file_location} onChange={setVersionField("file_location")} required />
                            </label>
                            <label>
                                Change note (optional)
                                <input value={newVersion.change_note} onChange={setVersionField("change_note")} />
                            </label>
                            <button type="submit">Add version</button>
                        </form>
                    </div>

                    <div className="box">
                        <h3>Session assignment</h3>
                        <label>
                            Session
                            <select value={sessionId} onChange={(event) => setSessionId(event.target.value)}>
                                <option value="">-- not scheduled --</option>
                                {sessions.map((session) => (
                                    <option key={session.session_id} value={session.session_id}>
                                        {session.title} ({session.session_date})
                                    </option>
                                ))}
                            </select>
                        </label>
                        <button type="button" onClick={assignSession}>Save session assignment</button>
                    </div>
                </>
            )}

            <div className="box">
                <h3>All papers ({papers.length})</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Title</th>
                            <th>Status</th>
                            <th>Track</th>
                            <th>Conference</th>
                            <th>Session</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {papers.map((paper) => (
                            <tr key={paper.paper_id}>
                                <td>{paper.title}</td>
                                <td>{paper.status}</td>
                                <td>{paper.track_name}</td>
                                <td>{paper.conference_acronym}</td>
                                <td>{sessionTitle(paper.session_id)}</td>
                                <td>
                                    <button onClick={() => edit(paper.paper_id)}>Edit</button>
                                    <button onClick={() => remove(paper.paper_id)}>Delete</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </>
    )
}

export default Papers

    