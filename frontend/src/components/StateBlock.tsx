type Props = {
  kind: 'loading' | 'empty' | 'error'
  title?: string
  description?: string
}

export function StateBlock({ kind, title, description }: Props) {
  const defaults = {
    loading: { icon: '◌', title: 'Loading…', description: 'Fetching the latest data.' },
    empty: { icon: '○', title: 'Nothing here yet', description: 'When something appears it will show up in this list.' },
    error: { icon: '!', title: 'Couldn’t load data', description: 'Check your connection or try again in a moment.' },
  }[kind]

  return (
    <div className="state" role="status">
      <div className="state__icon" aria-hidden>
        {defaults.icon}
      </div>
      <p className="state__title">{title ?? defaults.title}</p>
      <p className="state__desc">{description ?? defaults.description}</p>
    </div>
  )
}
