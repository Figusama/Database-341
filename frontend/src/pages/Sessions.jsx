import { useEffect, useState } from "react"
import { api } from "../api"

const EMPTY_FORM = {
    conference_id: "",
    title: "",
    session_date: "",
    start_time: "",
    end_time: "",
    room_label: "",
    chair_id: "",
}

const Sessions = () => {
    const [sessions, setSessions] = useState([])
    const [conferences, setConferences] = useState([])
    const [reviewers, setReviewers] = useState([])
    const [form, setForm] = useState(EMPTY_FORM)
    const [editingId, setEditingId] = useState(null)
    const [error, setError] = useState("")
    const [message, setMessage] = useState("")

    const load = () => {
        api.sessions.list()
            .then((data) => setSessions(data))
            .catch((error) => setError(error.message))
    }

    useEffect(() => {
        load()
        api.conferences()
            .then((data) => setConferences(data))
            .catch((error) => setError(error.message))
        api.reviewers()
            .then((data) => setReviewers(data))
            .catch((error) => setError(error.message))
    }, [])

    const set = (field) => {
        return (event) => {
            setForm({ ...form, [field]: event.target.value })
        }
    }

    const reset = () => {
        setForm(EMPTY_FORM)
        setEditingId(null)
    }

    const save = async (event) => {
        event.preventDefault()
        setError("")
        setMessage("")

        try {
            if (editingId) {
                await api.sessions.update(editingId, form)
                setMessage("Session updated")
            } else {
                await api.sessions.create(form)
                setMessage("Session created")
            }
            reset()
            load()
        } catch (error) {
            setError(error.message)
        }
    }

    const edit = async (id) => {
        setError("")
        setMessage("")
        try {
            const session = await api.sessions.get(id)
            setForm({
                conference_id: session.conference_id,
                title: session.title,
                session_date: session.session_date,
                start_time: session.start_time.slice(0, 5),
                end_time: session.end_time.slice(0, 5),
                room_label: session.room_label,
                chair_id: session.chair_id,
            })
            setEditingId(id)
        } catch (error) {
            setError(error.message)
        }
    }

    const remove = async (id) => {
        if (!confirm("Delete this session?")) return
        setError("")
        setMessage("")
        try {
            await api.sessions.remove(id)
            setMessage("Session deleted")
            load()
        } catch (error) {
            setError(error.message)
        }
    }

    const conferenceName = (id) => conferences.find((c) => c.conference_id === id)?.acronym ?? ""
    const chairName = (id) => {
        const r = reviewers.find((r) => r.reviewer_id === id)
        return r ? `${r.given_name} ${r.surname}` : ""
    }

    return (
        <>
            <h2>Sessions</h2>

            {error && <div className="error">Error: {error}</div>}
            {message && <div className="ok">{message}</div>}

            <form className="box" onSubmit={save}>
                <h3>{editingId ? "Edit session" : "Create session"}</h3>

                <label>
                    Conference
                    <select value={form.conference_id} onChange={set("conference_id")} required>
                        <option value="">-- choose --</option>
                        {conferences.map((conference) => (
                            <option key={conference.conference_id} value={conference.conference_id}>
                                {conference.acronym} ({conference.city})
                            </option>
                        ))}
                    </select>
                </label>

                <label>
                    Title
                    <input value={form.title} onChange={set("title")} required />
                </label>

                <label>
                    Date
                    <input type="date" value={form.session_date} onChange={set("session_date")} required />
                </label>

                <label>
                    Start time
                    <input type="time" value={form.start_time} onChange={set("start_time")} required />
                </label>

                <label>
                    End time
                    <input type="time" value={form.end_time} onChange={set("end_time")} required />
                </label>

                <label>
                    Room
                    <input value={form.room_label} onChange={set("room_label")} required />
                </label>

                <label>
                    Chair
                    <select value={form.chair_id} onChange={set("chair_id")} required>
                        <option value="">-- choose --</option>
                        {reviewers.map((reviewer) => (
                            <option key={reviewer.reviewer_id} value={reviewer.reviewer_id}>
                                {reviewer.given_name} {reviewer.surname}
                            </option>
                        ))}
                    </select>
                </label>

                <button type="submit">{editingId ? "Save changes" : "Create session"}</button>
                {editingId && (
                    <button type="button" onClick={reset}>
                        Cancel edit
                    </button>
                )}
            </form>

            <div className="box">
                <h3>All sessions ({sessions.length})</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Conference</th>
                            <th>Title</th>
                            <th>Date</th>
                            <th>Time</th>
                            <th>Room</th>
                            <th>Chair</th>
                            <th>Papers</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {sessions.map((session) => (
                            <tr key={session.session_id}>
                                <td>{conferenceName(session.conference_id)}</td>
                                <td>{session.title}</td>
                                <td>{session.session_date}</td>
                                <td>{session.start_time.slice(0, 5)}–{session.end_time.slice(0, 5)}</td>
                                <td>{session.room_label}</td>
                                <td>{chairName(session.chair_id)}</td>
                                <td>{session.papers.length}</td>
                                <td>
                                    <button onClick={() => edit(session.session_id)}>Edit</button>
                                    <button onClick={() => remove(session.session_id)}>Delete</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </>
    )
}

export default Sessions