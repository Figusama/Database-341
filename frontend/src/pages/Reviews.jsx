import {useEffect, useState} from 'react'
import {api} from '../api'


const today = () => new Date().toISOString().slice(0, 10)
const EMPTY_FORM = {
    paper_id: "", reviewer_id: "", overall_score: 3, recommendation: "accept",
    comments_for_authors: "", confidential_comments: "", review_submission_date: today(),
}


const Reviews = () => {
    const [reviews, setReviews] = useState([])
    const [papers, setPapers] = useState([])
    const [reviewers, setReviewers] = useState([])
    const [form, setForm] = useState(EMPTY_FORM)
    const [editingId, setEditingId] = useState(null)
    const [error, setError] = useState("")
    const [message, setMessage] = useState("")


    const load = () => {
    api.reviews.list()
        .then((data) => setReviews(data))
        .catch((error) => setError(error.message))
    }

    useEffect(() => {
        load()
        api.papers.list()
            .then((data) => setPapers(data))
            .catch((error) => setError(error.message))
        api.reviewers()
            .then((data) => setReviewers(data))
            .catch((error) => setError(error.message))
    }, [])
    
    
    const set = (field) => {
        return (event) => {
            setForm({ ...form, [field]: event.target.value})
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
            ...form,
            overall_score: Number(form.overall_score),
            confidential_comments: form.confidential_comments || null,
        }
        delete body.review_id

        try {
            if(editingId){
                await api.reviews.update(editingId, body)
                setMessage("Review Updated!")
            } else {
                await api.reviews.create(body)
                setMessage("Review Created!")
            }
            reset()
            load()
        } catch(error) {
            setError(error.message)
        }
    }

    const edit = async (id) => {
        setError("")
        setMessage("")

        try{
            const review = await api.reviews.get(id)
            setForm({
                ...EMPTY_FORM,
                ...review, 
                confidential_comments: review.confidential_comments ?? ""
            })
            setEditingId(id)
        } catch (error) {
            setError(error.message)
        }
    }

    const remove = async (id) => {
        if(!confirm("Delete this review?")) return
        setError("")
        setMessage("")
        try {
            await api.reviews.remove(id)
            setMessage("Review Deleted")
            load()
        } catch (error) {
            setError(error.message)
        }
    }


    return (
        <>
            <h2>Reviews</h2>

            {error && <div className="error">Error: {error}</div>}
            {message && <div className="ok">{message}</div>}

            <form className="box" onSubmit={save}>
                <h3>{editingId ? "Edit review" : "Create review"}</h3>

                <label>
                    Paper
                    <select value={form.paper_id} onChange={set("paper_id")} required>
                        <option value="">-- choose --</option>
                        {papers.map((paper) => (
                            <option key={paper.paper_id} value={paper.paper_id}>
                                {paper.title}
                            </option>
                        ))}
                    </select>
                </label>

                <label>
                    Reviewer
                    <select value={form.reviewer_id} onChange={set("reviewer_id")} required>
                        <option value="">-- choose --</option>
                        {reviewers.map((reviewer) => (
                            <option key={reviewer.reviewer_id} value={reviewer.reviewer_id}>
                                {reviewer.given_name} {reviewer.surname}
                            </option>
                        ))}
                    </select>
                </label>

                <label>
                    Overall score (1-5)
                    <input
                        type="number"
                        min="1"
                        max="5"
                        value={form.overall_score}
                        onChange={set("overall_score")}
                        required
                    />
                </label>

                <label>
                    Recommendation
                    <select value={form.recommendation} onChange={set("recommendation")}>
                        <option value="accept">accept</option>
                        <option value="reject">reject</option>
                    </select>
                </label>

                <label>
                    Comments for authors
                    <textarea
                        value={form.comments_for_authors}
                        onChange={set("comments_for_authors")}
                        required
                    />
                </label>

                <label>
                    Confidential comments (optional)
                    <textarea
                        value={form.confidential_comments}
                        onChange={set("confidential_comments")}
                    />
                </label>

                <label>
                    Submission date
                    <input
                        type="date"
                        value={form.review_submission_date}
                        onChange={set("review_submission_date")}
                        required
                    />
                </label>

                <button type="submit">{editingId ? "Save changes" : "Create review"}</button>
                {editingId && (
                    <button type="button" onClick={reset}>
                        Cancel edit
                    </button>
                )}
            </form>

            <div className="box">
                <h3>All reviews ({reviews.length})</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Paper</th>
                            <th>Reviewer</th>
                            <th>Score</th>
                            <th>Recommendation</th>
                            <th>Date</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {reviews.map((review) => (
                            <tr key={review.review_id}>
                                <td>{review.paper_title}</td>
                                <td>{review.reviewer_name}</td>
                                <td>{review.overall_score}</td>
                                <td>{review.recommendation}</td>
                                <td>{review.review_submission_date}</td>
                                <td>
                                    <button onClick={() => edit(review.review_id)}>Edit</button>
                                    <button onClick={() => remove(review.review_id)}>Delete</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </>
    )

} 

export default Reviews


