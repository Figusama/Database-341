import { useEffect, useState } from "react"
import { api } from "../api"

const EMPTY_FORM = {
    given_name: "",
    surname: "",
    email: "",
    affiliation: "",
    country: "",
    phone_number: "",

    is_author: false,
    orcid: "",
    research_areas: "",   

    is_reviewer: false,
    years_experience: 0,
    expertise: "",         
}


const toList = (text) => {
    const items = text
        .split(",")
        .map((item) => item.trim())
        .filter((item) => item !== "")
    return [...new Set(items)]
}

const Users = () => {
    const [users, setUsers] = useState([])
    const [form, setForm] = useState(EMPTY_FORM)
    const [editingId, setEditingId] = useState(null)
    const [error, setError] = useState("")
    const [message, setMessage] = useState("")

    const load = () => {
        api.users.list()
            .then((data) => setUsers(data))
            .catch((error) => setError(error.message))
    }

    useEffect(() => {
        load()
    }, [])

    
    const set = (field) => {
        return (event) => {
            setForm({ ...form, [field]: event.target.value})
        }
    }


    const toggle = (field) => {
        return (event) => {
            setForm({...form, [field]: event.target.checked})
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

        const body = {
            given_name: form.given_name,
            surname: form.surname,
            email: form.email,
            affiliation: form.affiliation,
            country: form.country,
            phone_number: form.phone_number,

            author: form.is_author
                ? { orcid: form.orcid || null, research_areas: toList(form.research_areas) }
                : null,

            reviewer: form.is_reviewer
                ? { years_experience: Number(form.years_experience), expertise: toList(form.expertise) }
                : null,
        }

        try {
            if(editingId){
                await api.users.update(editingId, body)
                setMessage("User Updated")
            } else {
                await api.users.create(body)
                setMessage("User created")
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
            const user = await api.users.get(id)
            setForm({
                given_name: user.given_name,
                surname: user.surname,
                email: user.email,
                affiliation: user.affiliation,
                country: user.country,
                phone_number: user.phone_number,

                is_author: user.author !== null,
                orcid: user.author?.orcid ?? "",
                research_areas: user.author ? user.author.research_areas.join(", ") : "",

                is_reviewer: user.reviewer !== null,
                years_experience: user.reviewer?.years_experience ?? 0,
                expertise: user.reviewer ? user.reviewer.expertise.join(", ") : "",
            })
            setEditingId(id)
        } catch(error) {
        setError(error.message)
        }
    }

    const remove = async (id) => {
        if (!confirm("Delete this user?")) return
        setError("")
        setMessage("")
        try {
            await api.users.remove(id)
            setMessage("User deleted")
            load()
        } catch (error) {
            setError(error.message)
        }
    }

    return (
        <>
            <h2>Users</h2>

            {error && <div className="error">Error: {error}</div>}
            {message && <div className="ok">{message}</div>}

            <form className="box" onSubmit={save}>
                <h3>{editingId ? "Edit user" : "Create user"}</h3>

                <label>
                    Given name
                    <input value={form.given_name} onChange={set("given_name")} required />
                </label>
                <label>
                    Surname
                    <input value={form.surname} onChange={set("surname")} required />
                </label>
                <label>
                    Email
                    <input type="email" value={form.email} onChange={set("email")} required />
                </label>
                <label>
                    Affiliation
                    <input value={form.affiliation} onChange={set("affiliation")} required />
                </label>
                <label>
                    Country
                    <input value={form.country} onChange={set("country")} required />
                </label>
                <label>
                    Phone number
                    <input value={form.phone_number} onChange={set("phone_number")} required />
                </label>

                <div className="box">
                    <label>
                        <input type="checkbox" checked={form.is_author} onChange={toggle("is_author")} />
                        Is author
                    </label>
                    {form.is_author && (
                        <>
                            <label>
                                ORCID (optional)
                                <input value={form.orcid} onChange={set("orcid")} />
                            </label>
                            <label>
                                Research areas (comma separated)
                                <input value={form.research_areas} onChange={set("research_areas")} required />
                            </label>
                        </>
                    )}
                </div>

                <div className="box">
                    <label>
                        <input type="checkbox" checked={form.is_reviewer} onChange={toggle("is_reviewer")} />
                        Is reviewer
                    </label>
                    {form.is_reviewer && (
                        <>
                            <label>
                                Years of experience
                                <input
                                    type="number"
                                    min="0"
                                    value={form.years_experience}
                                    onChange={set("years_experience")}
                                    required
                                />
                            </label>
                            <label>
                                Expertise (comma separated)
                                <input value={form.expertise} onChange={set("expertise")} required />
                            </label>
                        </>
                    )}
                </div>

                <button type="submit">{editingId ? "Save changes" : "Create user"}</button>
                {editingId && (
                    <button type="button" onClick={reset}>
                        Cancel edit
                    </button>
                )}
            </form>

            <div className="box">
                <h3>All users ({users.length})</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Author</th>
                            <th>Reviewer</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {users.map((user) => (
                            <tr key={user.user_id}>
                                <td>{user.given_name} {user.surname}</td>
                                <td>{user.email}</td>
                                <td>{user.is_author ? "yes" : ""}</td>
                                <td>{user.is_reviewer ? "yes" : ""}</td>
                                <td>
                                    <button onClick={() => edit(user.user_id)}>Edit</button>
                                    <button onClick={() => remove(user.user_id)}>Delete</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </>
    )
}

export default Users