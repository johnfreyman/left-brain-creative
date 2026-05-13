const projects = [
  {
    name: 'Kaizen Tracker',
    status: 'Prototype',
    description: 'A lightweight team management tool for attendance, session tracking, and player progress.',
    href: '/kaizen-tracker/',
  },
  {
    name: 'Idea Lab',
    status: 'Planning',
    description: 'A quiet workspace for sketching, comparing, and shaping new web project concepts.',
    href: '#',
  },
  {
    name: 'Build Notes',
    status: 'Soon',
    description: 'Short writeups on product decisions, design details, and what each project is teaching me.',
    href: '#',
  },
]

function App() {
  return (
    <main className="site-shell">
      <nav className="topbar" aria-label="Primary navigation">
        <a className="brand" href="/" aria-label="Left Brain Creative home">
          <span className="brand-mark">LBC</span>
          <span>leftbraincreative.xyz</span>
        </a>
        <a className="repo-link" href="https://github.com/jfreyman/left-brain-creative">
          GitHub
        </a>
      </nav>

      <section className="hero" aria-labelledby="page-title">
        <div className="hero-copy">
          <p className="eyebrow">Left Brain Creative</p>
          <h1 id="page-title">A home base for useful web projects.</h1>
          <p className="intro">
            Small, practical experiments in team tools, creative workflows, and the little systems that make good
            ideas easier to use.
          </p>
          <div className="hero-actions">
            <a className="primary-action" href="#projects">
              View projects
            </a>
            <a className="secondary-action" href="mailto:hello@leftbraincreative.xyz">
              Say hello
            </a>
          </div>
        </div>

        <div className="studio-preview" aria-label="Abstract preview of web project workspace">
          <div className="preview-window window-large">
            <span />
            <span />
            <span />
            <div className="preview-grid">
              <div />
              <div />
              <div />
              <div />
            </div>
          </div>
          <div className="preview-window window-small">
            <div className="metric-line" />
            <div className="metric-line short" />
            <div className="metric-bar" />
          </div>
        </div>
      </section>

      <section className="project-section" id="projects" aria-labelledby="projects-title">
        <div className="section-heading">
          <p className="eyebrow">Workbench</p>
          <h2 id="projects-title">Projects in motion</h2>
        </div>

        <div className="project-grid">
          {projects.map((project) => (
            <article className="project-card" key={project.name}>
              <div>
                <span className="status">{project.status}</span>
                <h3>{project.name}</h3>
                <p>{project.description}</p>
              </div>
              <a href={project.href} aria-label={`Open ${project.name}`}>
                Open
              </a>
            </article>
          ))}
        </div>
      </section>
    </main>
  )
}

export default App
