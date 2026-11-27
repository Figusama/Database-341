import { useState } from 'react'
import Users from "../src/pages/Users.jsx"
import Papers from "../src/pages/Papers.jsx"
import Reviews from "../src/pages/Reviews.jsx"
import Sessions from "../src/pages/Sessions.jsx"



const PAGES = {
  Users: Users,
  Papers: Papers,
  Reviews: Reviews,
  Sessions: Sessions
}

function App() {
  const [page, setPage] = useState("Reviews")
  const Page = PAGES[page]

  return (
    <>
      <nav>
        {Object.keys(PAGES).map((name) => (
          <button key={name} className={name === page ? "active" : ""} onClick={() => setPage(name)}>
            {name}
          </button>
        ))}
      </nav>
      <Page />
    </>
  )
}

export default App
