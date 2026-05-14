import React from "react";
import { motion } from "framer-motion";
import { ArrowRight, BrainCircuit, Code2, Palette, Rocket, Sparkles } from "lucide-react";

const heroImage = "/hero-image.png";
const projects = [
  {
    title: "Classroom Tools",
    description: "Interactive lessons, simulations, and utilities designed for curious learners.",
    icon: BrainCircuit,
  },
  {
    title: "Code Experiments",
    description: "Small apps, prototypes, and technical playgrounds built from useful ideas.",
    icon: Code2,
  },
  {
    title: "Creative Concepts",
    description: "Design sketches, brand ideas, visual systems, and half-formed sparks worth saving.",
    icon: Palette,
  },
];


export default function LeftBrainCreativeLandingPage() {
  return (
    <div className="min-h-screen bg-[#f7f3ec] text-zinc-900">
      <header className="sticky top-0 z-50 border-b border-zinc-900/10 bg-[#f7f3ec]/85 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="grid h-10 w-10 place-items-center rounded-2xl bg-zinc-950 text-white shadow-sm">
              <BrainCircuit className="h-5 w-5" />
            </div>
            <div className="leading-tight">
              <p className="text-lg font-black tracking-tight">leftbrain<span className="bg-gradient-to-r from-orange-500 via-fuchsia-500 to-cyan-500 bg-clip-text text-transparent">creative</span><span className="text-zinc-500">.xyz</span></p>
              <p className="text-xs uppercase tracking-[0.28em] text-zinc-500">Logic meets imagination</p>
            </div>
          </div>

          <nav className="hidden items-center gap-8 text-sm font-medium text-zinc-700 md:flex">
            <a href="#projects" className="hover:text-zinc-950">Projects</a>
            <a href="#ideas" className="hover:text-zinc-950">Ideas</a>
            <a href="#about" className="hover:text-zinc-950">About</a>
          </nav>
        </div>
      </header>

      <main>
        <section className="relative overflow-hidden px-6 py-20 md:py-28">
          <div className="absolute left-0 top-20 h-72 w-72 rounded-full bg-cyan-400/20 blur-3xl" />
          <div className="absolute right-0 top-40 h-80 w-80 rounded-full bg-fuchsia-400/20 blur-3xl" />
          <div className="absolute bottom-10 left-1/3 h-72 w-72 rounded-full bg-orange-400/20 blur-3xl" />

          <div className="mx-auto grid max-w-7xl items-center gap-12 lg:grid-cols-[1.05fr_0.95fr]">
            <motion.div
              initial={{ opacity: 0, y: 24 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7 }}
              className="relative z-10"
            >
              <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-zinc-900/10 bg-white/60 px-4 py-2 text-sm font-semibold shadow-sm backdrop-blur">
                <Sparkles className="h-4 w-4 text-orange-500" />
                Projects, prototypes, sparks, and systems
              </div>

              <h1 className="max-w-4xl text-5xl font-black leading-[0.95] tracking-tight md:text-7xl">
                Think in systems.
                <span className="block bg-gradient-to-r from-orange-500 via-fuchsia-500 to-cyan-500 bg-clip-text text-transparent">
                  Dream in color.
                </span>
              </h1>

              <p className="mt-7 max-w-2xl text-lg leading-8 text-zinc-700 md:text-xl">
                A personal creative lab for the things I am building, testing, teaching, designing, and dreaming up — where structured thinking gives wild ideas a place to grow.
              </p>

              <div className="mt-9 flex flex-col gap-4 sm:flex-row">
                <button className="flex h-12 items-center rounded-2xl bg-zinc-950 px-6 text-base text-white hover:bg-zinc-800">
                  Explore projects
                  <ArrowRight className="ml-2 h-4 w-4" />
                </button>
                <button className="h-12 rounded-2xl border border-zinc-300 bg-white/60 px-6 text-base hover:bg-white">
                  View idea vault
                </button>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, scale: 0.96 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.8, delay: 0.1 }}
              className="relative z-10"
            >
              <img
                src={heroImage}
                alt="Left Brain Creative Hero"
                className="w-full rounded-[2rem] shadow-2xl"
              />
            </motion.div>
          </div>
        </section>

        <section id="projects" className="px-6 py-20">
          <div className="mx-auto max-w-7xl">
            <div className="mb-10 flex flex-col justify-between gap-4 md:flex-row md:items-end">
              <div>
                <p className="mb-3 text-sm font-bold uppercase tracking-[0.3em] text-zinc-500">What lives here</p>
                <h2 className="text-4xl font-black tracking-tight md:text-5xl">A home for useful ideas.</h2>
              </div>
              <p className="max-w-xl text-zinc-600">
                Not every idea starts polished. This site gives experiments, classroom tools, code snippets, and creative sparks a place to become something real.
              </p>
            </div>

            <div className="grid gap-5 md:grid-cols-3">
              {projects.map((project) => {
                const Icon = project.icon;
                return (
                  <div key={project.title} className="group overflow-hidden rounded-[2rem] border-zinc-900/10 bg-white/75 shadow-sm transition hover:-translate-y-1 hover:shadow-xl">
                    <div className="p-7">
                      <div className="mb-8 grid h-14 w-14 place-items-center rounded-2xl bg-zinc-950 text-white transition group-hover:scale-110">
                        <Icon className="h-7 w-7" />
                      </div>
                      <h3 className="text-2xl font-black tracking-tight">{project.title}</h3>
                      <p className="mt-4 leading-7 text-zinc-600">{project.description}</p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </section>

        <section id="ideas" className="px-6 py-20">
          <div className="mx-auto max-w-7xl overflow-hidden rounded-[2.5rem] bg-zinc-950 p-8 text-white md:p-14">
            <div className="grid gap-10 lg:grid-cols-[0.85fr_1.15fr] lg:items-center">
              <div>
                <p className="mb-3 text-sm font-bold uppercase tracking-[0.3em] text-cyan-300">The idea vault</p>
                <h2 className="text-4xl font-black tracking-tight md:text-5xl">Where half-built thoughts are allowed to breathe.</h2>
              </div>
              <div className="grid gap-4 sm:grid-cols-2">
                {["Lesson seed", "Prototype", "Visual sketch", "Research rabbit hole"].map((item, index) => (
                  <div key={item} className="rounded-3xl border border-white/10 bg-white/10 p-5 backdrop-blur">
                    <p className="text-sm font-bold uppercase tracking-[0.25em] text-white/50">0{index + 1}</p>
                    <p className="mt-4 text-xl font-black">{item}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        <section id="about" className="px-6 py-20">
          <div className="mx-auto grid max-w-7xl gap-10 rounded-[2.5rem] border border-zinc-900/10 bg-white/70 p-8 shadow-sm md:p-14 lg:grid-cols-[1fr_1.2fr]">
            <div>
              <Rocket className="mb-6 h-10 w-10 text-orange-500" />
              <h2 className="text-4xl font-black tracking-tight">Born in the gap between the equation and the imagination.</h2>
            </div>
            <div className="space-y-6 text-lg leading-8 text-zinc-700">
              <p>
                leftbraincreative.xyz is a portfolio, workshop, notebook, and launchpad. It is for the projects that start as questions, become sketches, turn into systems, and sometimes grow into tools worth sharing.
              </p>
              <p>
                The brand is intentionally split: one side precise, organized, and analytical; the other expressive, colorful, and curious. Together, they make a place where creativity has structure and structure has personality.
              </p>
            </div>
          </div>
        </section>
      </main>

      <footer className="border-t border-zinc-900/10 px-6 py-8">
        <div className="mx-auto flex max-w-7xl flex-col justify-between gap-4 text-sm text-zinc-500 md:flex-row md:items-center">
          <p>© 2026 leftbraincreative.xyz</p>
          <p>Logic builds. Creativity inspires.</p>
        </div>
      </footer>
    </div>
  );
}
