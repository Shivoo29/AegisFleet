import { useState, type FormEvent } from 'react'

export type Me = { user: string; role: 'dev' | 'judge' }

/** Login page: dev signs in with the console password, judges with the judge password. */
export default function Login({ onLogin }: { onLogin: (me: Me) => void }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)

  async function submit(e: FormEvent) {
    e.preventDefault()
    setBusy(true)
    setError(null)
    try {
      const res = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ username: username.trim(), password }),
      })
      if (!res.ok) throw new Error(res.status === 401 ? 'Wrong username or password.' : `Login failed (${res.status}).`)
      onLogin(await res.json())
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed.')
      setPassword('')
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="login">
      <form className="login__card" onSubmit={submit}>
        <div className="login__brand">
          <svg className="login__mark" viewBox="0 0 32 32" aria-hidden="true">
            <path d="M16 3.5 26 7.3v7.3c0 6.2-3.8 11.1-10 14.1-6.2-3-10-7.9-10-14.1V7.3L16 3.5Z"
              fill="none" stroke="currentColor" strokeLinejoin="round" strokeWidth="1.7" />
            <path d="m10.5 15.8 3.6 3.6 7.4-7.4" fill="none" stroke="currentColor"
              strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
          </svg>
          <div>
            <h1 className="login__title">AegisFleet</h1>
            <p className="login__subtitle">Get paid. Stay paid.</p>
          </div>
        </div>

        <label className="login__field">
          <span>Username</span>
          <input autoFocus autoComplete="username" value={username} placeholder="judge"
            onChange={(e) => setUsername(e.target.value)} required />
        </label>
        <label className="login__field">
          <span>Password</span>
          <input type="password" autoComplete="current-password" value={password}
            onChange={(e) => setPassword(e.target.value)} required />
        </label>

        {error && <p className="login__error" role="alert">{error}</p>}

        <button className="btn btn--primary login__submit" type="submit" disabled={busy}>
          {busy ? 'Signing in…' : 'Sign in'}
        </button>
        <p className="login__hint">Judges: use the credentials from the submission's testing instructions.</p>
      </form>
    </div>
  )
}
