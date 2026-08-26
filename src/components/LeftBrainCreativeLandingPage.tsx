const heroImage = "/hero-image.webp";

const heroImageAlt =
  "leftbraincreative.xyz lockup — a brain drawn half as circuitry, half as brushstrokes, with the line “Logic builds. Creativity inspires.”";

function BrandMark() {
  return (
    <svg width="32" height="32" viewBox="0 0 24 24" className="flex-none" aria-hidden="true">
      <defs>
        <linearGradient id="lbcMark" x1="0" y1="1" x2="1" y2="0">
          <stop offset="0" stopColor="#d946ef" />
          <stop offset="1" stopColor="#06b6d4" />
        </linearGradient>
      </defs>
      <path
        d="M9 3.5H4.5v17H9"
        fill="none"
        stroke="#18181b"
        strokeWidth="2.2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M15 3.5h4.5v17H15"
        fill="none"
        stroke="url(#lbcMark)"
        strokeWidth="2.2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path d="M12 8v8" fill="none" stroke="#18181b" strokeWidth="2.2" strokeLinecap="round" />
    </svg>
  );
}

function ArrowRight() {
  return (
    <svg
      width="16"
      height="16"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d="M5 12h13" />
      <path d="M13 6l6 6-6 6" />
    </svg>
  );
}

const shell = "mx-auto max-w-[1180px]";
const kicker =
  "font-grotesk text-[11px] font-medium uppercase tracking-[0.26em] text-[#6b6b73]";
const sectionHeading =
  "font-grotesk text-[clamp(30px,3.4vw,42px)] font-medium leading-[1.08] tracking-[-0.025em] text-balance";
const bodyCopy = "text-[19px] font-light leading-[1.7] text-zinc-700 text-pretty";
const sectionGrid =
  "grid grid-cols-1 gap-10 border-t border-zinc-900/12 pt-16 wide:grid-cols-[0.85fr_1.15fr] wide:items-start wide:gap-16";

export default function LeftBrainCreativeLandingPage() {
  return (
    <div className="min-h-screen bg-[#f7f3ec] text-zinc-900">
      <header className="sticky top-0 z-50 border-b border-zinc-900/10 bg-[#f7f3ec]/88 backdrop-blur-[16px]">
        <div className={`${shell} flex flex-wrap items-center justify-between gap-6 px-7 py-4`}>
          <div className="flex items-center gap-3">
            <BrandMark />
            <div className="leading-[1.25]">
              <p className="font-grotesk text-[19px] font-bold tracking-[-0.02em]">
                leftbrain
                <span className="bg-[linear-gradient(96deg,#f97316,#d946ef_52%,#06b6d4)] bg-clip-text text-transparent">
                  creative
                </span>
                <span className="text-zinc-400">.xyz</span>
              </p>
              <p className="mt-[3px] font-grotesk text-[10px] font-medium uppercase tracking-[0.26em] text-[#6b6b73]">
                Logic meets imagination
              </p>
            </div>
          </div>

          <nav className="flex items-center gap-7 font-grotesk text-[14px] font-medium text-zinc-700">
            <a href="#workshop">Workshop</a>
            <a href="#about">About</a>
          </nav>
        </div>
      </header>

      <main>
        <section className="relative overflow-hidden px-7">
          <div aria-hidden="true">
            <div className="absolute -left-[60px] top-[60px] h-[300px] w-[300px] rounded-full bg-[rgba(6,182,212,0.16)] blur-[70px]" />
            <div className="absolute -right-[40px] top-[220px] h-[320px] w-[320px] rounded-full bg-[rgba(217,70,239,0.14)] blur-[80px]" />
          </div>

          <div
            className={`${shell} relative z-[1] grid grid-cols-1 gap-10 pt-24 pb-[84px] wide:grid-cols-[1.05fr_0.95fr] wide:items-center wide:gap-16`}
          >
            <div>
              <p className="mb-[22px] inline-flex items-center gap-[9px] font-grotesk text-[11px] font-medium uppercase tracking-[0.2em] text-[#6b6b73]">
                <span className="inline-block h-[2px] w-[26px] bg-[linear-gradient(90deg,#f97316,#d946ef)]" />
                Projects, prototypes, sparks, and systems
              </p>

              <h1 className="font-grotesk text-[clamp(48px,6.4vw,86px)] font-bold leading-[0.94] tracking-[-0.035em] text-balance">
                Think in systems.
                <span className="block bg-[linear-gradient(96deg,#f97316,#d946ef_50%,#06b6d4)] bg-clip-text text-transparent">
                  Dream in color.
                </span>
              </h1>

              <p className="mt-[30px] max-w-[34em] text-[20px] font-light leading-[1.65] text-zinc-700 text-pretty">
                A personal creative lab for the things I am building, testing, teaching, designing,
                and dreaming up — where structured thinking gives wild ideas a place to grow.
              </p>

              <div className="mt-[38px] flex flex-wrap items-center gap-[22px]">
                <a
                  href="#workshop"
                  className="inline-flex h-[50px] items-center gap-[10px] rounded-xl bg-zinc-900 px-[26px] font-grotesk text-[15px] font-medium text-[#f7f3ec] hover:bg-zinc-700 hover:text-[#f7f3ec]"
                >
                  What I am working on
                  <ArrowRight />
                </a>
                <a
                  href="#about"
                  className="border-b border-zinc-900/25 pb-[2px] font-grotesk text-[15px] font-medium text-zinc-700 hover:border-orange-700 hover:text-orange-700"
                >
                  Read the premise
                </a>
              </div>
            </div>

            <div>
              <img
                src={heroImage}
                width="2772"
                height="934"
                alt={heroImageAlt}
                className="block h-auto w-full rounded-[20px] shadow-[0_24px_60px_-28px_rgba(24,24,27,0.34)]"
              />
            </div>
          </div>
        </section>

        <section id="workshop" className="px-7 pb-24">
          <div className={`${shell} ${sectionGrid}`}>
            <div>
              <p className={`mb-[14px] ${kicker}`}>Currently</p>
              <h2 className={sectionHeading}>The workshop is busy.</h2>
            </div>
            <div className="max-w-[38em]">
              <p className={bodyCopy}>
                There is a lot in progress right now — classroom tools, a few small apps, and
                several ideas still at the sketch stage.
              </p>
              <div className="mt-[34px] flex w-fit items-center gap-[13px] rounded-xl border border-zinc-900/12 bg-white/60 px-5 py-[15px]">
                <span className="relative inline-flex h-[9px] w-[9px] flex-none">
                  <span className="lbc-pulse absolute inset-0 rounded-full bg-orange-500" />
                  <span className="relative h-[9px] w-[9px] rounded-full bg-orange-500" />
                </span>
                <p className="font-grotesk text-[13px] font-medium tracking-[0.01em] text-zinc-700">
                  Builds in progress
                </p>
              </div>
            </div>
          </div>
        </section>

        <section id="about" className="px-7 pb-26">
          <div className={`${shell} ${sectionGrid}`}>
            <div>
              <p className={`mb-[14px] ${kicker}`}>The premise</p>
              <h2 className={sectionHeading}>
                Born in the gap between the equation and the imagination.
              </h2>
            </div>
            <div className="flex max-w-[38em] flex-col gap-6">
              <p className={bodyCopy}>
                leftbraincreative.xyz is a portfolio, workshop, notebook, and launchpad. It is for
                the projects that start as questions, become sketches, turn into systems, and
                sometimes grow into tools worth sharing.
              </p>
              <p className={bodyCopy}>
                The brand is intentionally split: one side precise, organized, and analytical; the
                other expressive, colorful, and curious. Together, they make a place where
                creativity has structure and structure has personality.
              </p>
            </div>
          </div>
        </section>
      </main>

      <footer className="border-t border-zinc-900/10 px-7 py-[26px]">
        <div
          className={`${shell} flex flex-wrap items-center justify-between gap-5 font-grotesk text-[13px] text-[#6b6b73]`}
        >
          <p>© 2026 leftbraincreative.xyz</p>
          <p>Logic builds. Creativity inspires.</p>
        </div>
      </footer>
    </div>
  );
}
