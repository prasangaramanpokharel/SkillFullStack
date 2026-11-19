#!/usr/bin/env node

/**
 * SkillFullStack CLI
 * Universal AI Agent Skills installer for Claude Code, Cursor, Antigravity, Windsurf, & Copilot.
 * 
 * GitHub: https://github.com/prasangaramanpokharel/skills
 * NPM: skillfullstack
 */

import fs from 'fs';
import { promises as fsp } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PKG_ROOT = path.resolve(__dirname, '..');
const REPO_RAW = 'https://raw.githubusercontent.com/prasangaramanpokharel/skills/main';

// ANSI color helpers (zero external dependencies)
const c = {
  reset: '\x1b[0m',
  bold: '\x1b[1m',
  dim: '\x1b[2m',
  cyan: '\x1b[36m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  red: '\x1b[31m',
  gray: '\x1b[90m',
};

// Load catalog
function loadCatalog() {
  const localCatalog = path.join(PKG_ROOT, '.skillsRegistry', 'catalog.json');
  if (fs.existsSync(localCatalog)) {
    try {
      return JSON.parse(fs.readFileSync(localCatalog, 'utf8'));
    } catch (err) {
      // Fallback
    }
  }
  return { skills: [] };
}

// Auto-detect project environment
function detectAgents() {
  const detected = [];
  const cwd = process.cwd();
  if (fs.existsSync(path.join(cwd, '.claude')) || fs.existsSync(path.join(cwd, '.claude.json')) || fs.existsSync(path.join(cwd, 'CLAUDE.md'))) detected.push('claude');
  if (fs.existsSync(path.join(cwd, '.cursor')) || fs.existsSync(path.join(cwd, '.cursorrules')) || fs.existsSync(path.join(cwd, '.cursor/rules'))) detected.push('cursor');
  if (fs.existsSync(path.join(cwd, '.gemini')) || fs.existsSync(path.join(cwd, '.gemini/antigravity'))) detected.push('antigravity');
  if (fs.existsSync(path.join(cwd, '.opencode')) || fs.existsSync(path.join(cwd, 'opencode.json')) || fs.existsSync(path.join(cwd, '.codex'))) detected.push('opencode');
  if (fs.existsSync(path.join(cwd, '.windsurf')) || fs.existsSync(path.join(cwd, '.windsurfrules')) || fs.existsSync(path.join(cwd, '.codeium'))) detected.push('windsurf');
  if (fs.existsSync(path.join(cwd, '.github')) || fs.existsSync(path.join(cwd, '.github/copilot-instructions.md'))) detected.push('copilot');
  if (fs.existsSync(path.join(cwd, '.agent')) || fs.existsSync(path.join(cwd, '.agents'))) detected.push('agent');
  return detected;
}

// Normalize agent name aliases
function normalizeAgentName(raw) {
  if (!raw) return 'agent';
  const name = raw.toLowerCase().trim();
  if (['claude', 'claude-code', 'claudecode', 'anthropic'].includes(name)) return 'claude';
  if (['cursor'].includes(name)) return 'cursor';
  if (['gemini', 'antigravity', 'google'].includes(name)) return 'antigravity';
  if (['opencode', 'codex', 'openai', 'interpreter'].includes(name)) return 'opencode';
  if (['windsurf', 'codeium', 'cascade'].includes(name)) return 'windsurf';
  if (['copilot', 'github', 'gh-copilot'].includes(name)) return 'copilot';
  if (['agent', 'agents', 'universal', 'openagent'].includes(name)) return 'agent';
  if (name === 'all') return 'all';
  return name;
}

function resolveInstallTarget(skillName, agent, customDir = null) {
  const cwd = process.cwd();
  if (customDir) {
    return {
      targetDir: path.resolve(cwd, customDir, skillName),
      targetFile: path.resolve(cwd, customDir, skillName, 'SKILL.md'),
      agent: 'custom',
    };
  }

  const normalized = normalizeAgentName(agent);

  switch (normalized) {
    case 'antigravity':
      return {
        targetDir: path.join(cwd, '.gemini/antigravity/skills', skillName),
        targetFile: path.join(cwd, '.gemini/antigravity/skills', skillName, 'SKILL.md'),
        agent: 'antigravity',
      };
    case 'claude':
      return {
        targetDir: path.join(cwd, '.claude/skills', skillName),
        targetFile: path.join(cwd, '.claude/skills', skillName, 'SKILL.md'),
        cmdDir: path.join(cwd, '.claude/commands'),
        cmdFile: path.join(cwd, '.claude/commands', `${skillName}.md`),
        agent: 'claude',
      };
    case 'cursor':
      return {
        targetDir: path.join(cwd, '.cursor/skills', skillName),
        targetFile: path.join(cwd, '.cursor/skills', skillName, 'SKILL.md'),
        ruleDir: path.join(cwd, '.cursor/rules'),
        ruleFile: path.join(cwd, '.cursor/rules', `${skillName}.mdc`),
        agent: 'cursor',
      };
    case 'opencode':
      return {
        targetDir: path.join(cwd, '.opencode/skills', skillName),
        targetFile: path.join(cwd, '.opencode/skills', skillName, 'SKILL.md'),
        agent: 'opencode',
      };
    case 'windsurf':
      return {
        targetDir: path.join(cwd, '.windsurf/skills', skillName),
        targetFile: path.join(cwd, '.windsurf/skills', skillName, 'SKILL.md'),
        ruleDir: path.join(cwd, '.windsurf/rules'),
        ruleFile: path.join(cwd, '.windsurf/rules', `${skillName}.md`),
        agent: 'windsurf',
      };
    case 'copilot':
      return {
        targetDir: path.join(cwd, '.github/skills', skillName),
        targetFile: path.join(cwd, '.github/skills', skillName, 'SKILL.md'),
        agent: 'copilot',
      };
    case 'agent':
    default:
      return {
        targetDir: path.join(cwd, '.agent/skills', skillName),
        targetFile: path.join(cwd, '.agent/skills', skillName, 'SKILL.md'),
        agent: 'agent',
      };
  }
}

// -------------------------------------------------------------
// Commands
// -------------------------------------------------------------

async function cmdList(args, catalog) {
  const taxonomyFilter = args.taxonomy || args.t;
  const asJson = args.json;

  let skills = catalog.skills || [];
  if (taxonomyFilter) {
    skills = skills.filter((s) => s.taxonomy.toLowerCase() === taxonomyFilter.toLowerCase());
  }

  if (asJson) {
    console.log(JSON.stringify(skills, null, 2));
    return;
  }

  console.log(`\n${c.bold}${c.cyan}📦 SkillFullStack — Available AI Agent Skills (${skills.length})${c.reset}\n`);

  const groups = {};
  for (const s of skills) {
    if (!groups[s.taxonomy]) groups[s.taxonomy] = [];
    groups[s.taxonomy].push(s);
  }

  for (const [tax, list] of Object.entries(groups)) {
    console.log(`${c.bold}${c.yellow}▶ ${tax.toUpperCase()}${c.reset} ${c.gray}(${list.length})${c.reset}`);
    for (const item of list) {
      console.log(`  ${c.green}${item.name.padEnd(26)}${c.reset} ${c.dim}${item.version || 'latest'}${c.reset}`);
      console.log(`  ${c.gray}${item.description.slice(0, 85)}...${c.reset}`);
    }
    console.log('');
  }

  console.log(`${c.dim}To install a skill: ${c.cyan}npx skillfullstack add <skill-name> [--agent=<agent>]${c.reset}\n`);
}

async function cmdSearch(query, catalog) {
  if (!query) {
    console.log(`${c.red}Error: Search query required. Example: npx skillfullstack search nextjs${c.reset}`);
    return;
  }

  const q = query.toLowerCase();
  const matches = (catalog.skills || []).filter(
    (s) =>
      s.name.toLowerCase().includes(q) ||
      s.taxonomy.toLowerCase().includes(q) ||
      s.description.toLowerCase().includes(q)
  );

  console.log(`\n${c.bold}🔍 Search results for "${query}" (${matches.length} found):${c.reset}\n`);

  if (matches.length === 0) {
    console.log(`  ${c.gray}No skills matched your query.${c.reset}\n`);
    return;
  }

  for (const s of matches) {
    console.log(`  • ${c.green}${c.bold}${s.name}${c.reset} ${c.gray}[${s.taxonomy}] (${s.version || 'latest'})${c.reset}`);
    console.log(`    ${s.description}\n`);
  }
}

async function cmdInfo(skillName, catalog) {
  if (!skillName) {
    console.log(`${c.red}Error: Skill name required. Example: npx skillfullstack info astro${c.reset}`);
    return;
  }

  const skill = (catalog.skills || []).find((s) => s.name.toLowerCase() === skillName.toLowerCase());
  if (!skill) {
    console.log(`${c.red}Error: Skill "${skillName}" not found in catalog.${c.reset}`);
    return;
  }

  console.log(`\n${c.bold}${c.cyan}ℹ️  Skill: ${skill.name}${c.reset}`);
  console.log(`  ${c.bold}Taxonomy:${c.reset}       ${skill.taxonomy}`);
  console.log(`  ${c.bold}Version:${c.reset}        ${skill.version || 'latest'}`);
  console.log(`  ${c.bold}Path:${c.reset}           ${skill.path}`);
  console.log(`  ${c.bold}Verified Date:${c.reset}  ${skill.verified_date || 'N/A'}`);
  console.log(`  ${c.bold}Official Docs:${c.reset}  ${skill.docs || 'N/A'}`);
  console.log(`\n  ${c.bold}Description:${c.reset}\n  ${skill.description}\n`);

  const localAssetDir = path.join(PKG_ROOT, skill.path, 'assets');
  const hasAssets = fs.existsSync(localAssetDir);
  console.log(`  ${c.bold}Offline Assets:${c.reset} ${hasAssets ? c.green + '✓ Bundled (High-Accuracy)' : c.gray + 'Remote only'}${c.reset}`);
  console.log(`\n  ${c.bold}Install command:${c.reset} ${c.cyan}npx skillfullstack add ${skill.name}${c.reset}\n`);
}

async function installSingleSkill(skillName, catalog, options = {}) {
  const skill = (catalog.skills || []).find((s) => s.name.toLowerCase() === skillName.toLowerCase());
  if (!skill) {
    throw new Error(`Skill "${skillName}" not found in catalog.`);
  }

  const agentsToInstall = [];
  if (options.agent === 'all') {
    agentsToInstall.push('claude', 'cursor', 'antigravity', 'opencode', 'windsurf', 'copilot', 'agent');
  } else if (options.agent) {
    agentsToInstall.push(normalizeAgentName(options.agent));
  } else {
    const detected = detectAgents();
    if (detected.length > 0) {
      agentsToInstall.push(...detected);
    } else {
      agentsToInstall.push('agent');
    }
  }

  const localSkillDir = path.join(PKG_ROOT, skill.path);
  const hasLocalDir = fs.existsSync(localSkillDir);

  for (const agent of agentsToInstall) {
    const target = resolveInstallTarget(skill.name, agent, options.dir);
    await fsp.mkdir(target.targetDir, { recursive: true });

    if (hasLocalDir) {
      // 1. Copy the ENTIRE skill folder (SKILL.md, references/, assets/, scripts/, evals/, policies/, templates/)
      await fsp.cp(localSkillDir, target.targetDir, { recursive: true });
    } else {
      // Remote fallback: Fetch SKILL.md
      const remoteUrl = `${REPO_RAW}/${skill.path}/SKILL.md`;
      const res = await fetch(remoteUrl);
      if (!res.ok) throw new Error(`Failed to fetch ${remoteUrl} (HTTP ${res.status})`);
      const content = await res.text();
      await fsp.writeFile(target.targetFile, content, 'utf8');
    }

    // 2. Special handling for Claude Code: also register slash command
    if (target.cmdFile && target.cmdDir) {
      await fsp.mkdir(target.cmdDir, { recursive: true });
      const skillMdContent = await fsp.readFile(path.join(target.targetDir, 'SKILL.md'), 'utf8');
      await fsp.writeFile(target.cmdFile, skillMdContent, 'utf8');
    }

    // 3. Special handling for Cursor: also create .mdc rule file
    if (target.ruleFile && target.ruleDir && target.agent === 'cursor') {
      await fsp.mkdir(target.ruleDir, { recursive: true });
      const skillMdContent = await fsp.readFile(path.join(target.targetDir, 'SKILL.md'), 'utf8');
      const cursorContent = `---
description: ${skill.description}
globs: *
alwaysApply: false
---

${skillMdContent}`;
      await fsp.writeFile(target.ruleFile, cursorContent, 'utf8');
    }

    // 4. Special handling for Windsurf: also create rule file
    if (target.ruleFile && target.ruleDir && target.agent === 'windsurf') {
      await fsp.mkdir(target.ruleDir, { recursive: true });
      const skillMdContent = await fsp.readFile(path.join(target.targetDir, 'SKILL.md'), 'utf8');
      await fsp.writeFile(target.ruleFile, skillMdContent, 'utf8');
    }

    // List installed subdirectories for transparency
    const installedItems = ['SKILL.md'];
    if (fs.existsSync(path.join(target.targetDir, 'references'))) installedItems.push('references/');
    if (fs.existsSync(path.join(target.targetDir, 'assets'))) installedItems.push('assets/');
    if (fs.existsSync(path.join(target.targetDir, 'scripts'))) installedItems.push('scripts/');
    if (fs.existsSync(path.join(target.targetDir, 'evals'))) installedItems.push('evals/');
    if (fs.existsSync(path.join(target.targetDir, 'policies'))) installedItems.push('policies/');

    console.log(`  ${c.green}✓${c.reset} Installed ${c.bold}${skill.name}${c.reset} for ${c.cyan}${agent}${c.reset}`);
    console.log(`    ${c.gray}→ ${path.relative(process.cwd(), target.targetDir)}/ [${installedItems.join(', ')}]${c.reset}`);
    if (target.cmdFile) {
      console.log(`    ${c.gray}→ Slash command: ${path.relative(process.cwd(), target.cmdFile)} (/${skill.name})${c.reset}`);
    }
    if (target.ruleFile) {
      console.log(`    ${c.gray}→ ${target.agent === 'cursor' ? 'Cursor rule' : 'Windsurf rule'}: ${path.relative(process.cwd(), target.ruleFile)}${c.reset}`);
    }
  }
}

async function cmdAdd(skillNames, catalog, options) {
  if (!skillNames || skillNames.length === 0) {
    console.log(`${c.red}Error: Specify at least one skill to add.${c.reset}`);
    console.log(`Example: ${c.cyan}npx skillfullstack add nextjs astro cloudflare${c.reset}\n`);
    return;
  }

  console.log(`\n${c.bold}🚀 Installing ${skillNames.length} skill(s)...${c.reset}\n`);

  for (const name of skillNames) {
    try {
      await installSingleSkill(name, catalog, options);
    } catch (err) {
      console.log(`  ${c.red}✗ Failed to install "${name}": ${err.message}${c.reset}`);
    }
  }

  console.log(`\n${c.green}${c.bold}✨ All requested skills have been configured!${c.reset}\n`);
}

async function cmdInit(catalog) {
  console.log(`\n${c.bold}${c.cyan}🛠️  SkillFullStack Project Initializer${c.reset}\n`);
  const cwd = process.cwd();

  // 1. Detect Agents
  const detectedAgents = detectAgents();
  console.log(`${c.bold}Detected AI Agent Environments:${c.reset}`);
  if (detectedAgents.length === 0) {
    console.log(`  ${c.gray}None detected. Will default to open Agent Skills standard (${c.cyan}.agent/skills/${c.gray})${c.reset}`);
  } else {
    for (const a of detectedAgents) {
      console.log(`  ${c.green}✓ ${a}${c.reset}`);
    }
  }
  console.log('');

  // 2. Detect Tech Stack
  const recommendedSkills = new Set();
  const pkgJsonPath = path.join(cwd, 'package.json');
  if (fs.existsSync(pkgJsonPath)) {
    try {
      const pkg = JSON.parse(fs.readFileSync(pkgJsonPath, 'utf8'));
      const deps = { ...(pkg.dependencies || {}), ...(pkg.devDependencies || {}) };
      if (deps['next']) recommendedSkills.add('nextjs');
      if (deps['astro']) recommendedSkills.add('astro');
      if (deps['tailwindcss'] || deps['@radix-ui/react-slot']) recommendedSkills.add('shadcn-ui');
      if (deps['ai'] || deps['@ai-sdk/react']) recommendedSkills.add('generativeUi');
      if (deps['@cloudflare/workers-types'] || deps['wrangler'] || deps['@cloudflare/config']) recommendedSkills.add('cloudflare');
      if (deps['@upstash/redis'] || deps['@upstash/ratelimit']) recommendedSkills.add('upstash');
      if (deps['inngest'] || deps['@trigger.dev/sdk']) recommendedSkills.add('durableBackgroundJobs');
      if (deps['typescript'] || deps['react']) recommendedSkills.add('tsxReactStandard');
    } catch (e) {
      // Ignore
    }
  }

  if (fs.existsSync(path.join(cwd, 'go.mod'))) recommendedSkills.add('golangStandard');
  if (fs.existsSync(path.join(cwd, 'pyproject.toml')) || fs.existsSync(path.join(cwd, 'requirements.txt'))) recommendedSkills.add('pythonStandard');
  if (fs.existsSync(path.join(cwd, '.github'))) {
    recommendedSkills.add('githubAction');
    recommendedSkills.add('githubQuality');
  }
  if (fs.existsSync(path.join(cwd, '.git'))) recommendedSkills.add('gitWorkflow');

  console.log(`${c.bold}Recommended Skills for your Stack:${c.reset}`);
  if (recommendedSkills.size === 0) {
    console.log(`  ${c.gray}No specific framework detected. Recommended foundational skills:${c.reset}`);
    recommendedSkills.add('testDrivenDevelopment');
    recommendedSkills.add('gitWorkflow');
    recommendedSkills.add('apiEngineering');
  }

  const recList = Array.from(recommendedSkills);
  for (const r of recList) {
    console.log(`  ${c.yellow}★ ${r}${c.reset}`);
  }

  console.log(`\nTo install all recommended skills for your project:`);
  console.log(`  ${c.cyan}npx skillfullstack add ${recList.join(' ')}${c.reset}\n`);
}

function showHelp() {
  console.log(`
${c.bold}${c.cyan}SkillFullStack CLI${c.reset} — Universal AI Agent Skills Installer

${c.bold}USAGE${c.reset}
  $ ${c.cyan}npx skillfullstack${c.reset} <command> [options]
  $ ${c.cyan}sfs${c.reset} <command> [options]

${c.bold}COMMANDS${c.reset}
  ${c.green}add, install${c.reset} <skill...>    Install one or more skills (copies SKILL.md, references, assets, etc.)
  ${c.green}list, ls${c.reset}                   List all 25+ verified skills across all domains
  ${c.green}search${c.reset} <query>             Search skills by keyword, framework, or capability
  ${c.green}info${c.reset} <skill>               Show detailed documentation, slash commands, & metadata
  ${c.green}init${c.reset}                       Inspect repository and recommend skills for your stack

${c.bold}OPTIONS${c.reset}
  ${c.yellow}-a, --agent <name>${c.reset}        Target agent: ${c.dim}claude, cursor, gemini, antigravity, opencode, codex, windsurf, copilot, agent, all${c.reset}
  ${c.yellow}-d, --dir <path>${c.reset}          Custom destination folder
  ${c.yellow}-t, --taxonomy <name>${c.reset}     Filter list by category (frontend, backend, github, etc.)
  ${c.yellow}--json${c.reset}                    Output catalog as JSON
  ${c.yellow}-h, --help${c.reset}                Display help guide
  ${c.yellow}-v, --version${c.reset}             Display version

${c.bold}EXAMPLES${c.reset}
  $ ${c.cyan}npx skillfullstack add nextjs${c.reset}
  $ ${c.cyan}npx skillfullstack add nextjs --agent=cursor${c.reset}
  $ ${c.cyan}npx skillfullstack add nextjs --agent=gemini${c.reset}
  $ ${c.cyan}npx skillfullstack add nextjs --agent=opencode${c.reset}
  $ ${c.cyan}npx skillfullstack add astro cloudflare --agent=all${c.reset}
  $ ${c.cyan}npx skillfullstack list --taxonomy frontend${c.reset}
  $ ${c.cyan}npx skillfullstack search graphql${c.reset}
  $ ${c.cyan}npx skillfullstack init${c.reset}
`);
}

// -------------------------------------------------------------
// Main Entrypoint
// -------------------------------------------------------------

async function main() {
  const rawArgs = process.argv.slice(2);
  const command = rawArgs[0];

  if (!command || command === '-h' || command === '--help' || command === 'help') {
    showHelp();
    return;
  }

  if (command === '-v' || command === '--version' || command === 'version') {
    const pkg = JSON.parse(fs.readFileSync(path.join(PKG_ROOT, 'package.json'), 'utf8'));
    console.log(`v${pkg.version}`);
    return;
  }

  const catalog = loadCatalog();

  const options = {
    agent: null,
    dir: null,
    taxonomy: null,
    json: false,
  };

  const positional = [];
  for (let i = 1; i < rawArgs.length; i++) {
    const arg = rawArgs[i];
    if (arg.startsWith('--agent=')) {
      options.agent = arg.split('=')[1];
    } else if (arg === '-a' || arg === '--agent') {
      options.agent = rawArgs[++i];
    } else if (arg.startsWith('--dir=')) {
      options.dir = arg.split('=')[1];
    } else if (arg === '-d' || arg === '--dir') {
      options.dir = rawArgs[++i];
    } else if (arg.startsWith('--taxonomy=') || arg.startsWith('-t=')) {
      options.taxonomy = arg.split('=')[1];
    } else if (arg === '-t' || arg === '--taxonomy') {
      options.taxonomy = rawArgs[++i];
    } else if (arg === '--json') {
      options.json = true;
    } else if (!arg.startsWith('-')) {
      positional.push(arg);
    }
  }

  switch (command) {
    case 'add':
    case 'install':
      await cmdAdd(positional, catalog, options);
      break;
    case 'list':
    case 'ls':
      await cmdList(options, catalog);
      break;
    case 'search':
    case 'find':
      await cmdSearch(positional[0], catalog);
      break;
    case 'info':
    case 'show':
      await cmdInfo(positional[0], catalog);
      break;
    case 'init':
      await cmdInit(catalog);
      break;
    default:
      console.log(`${c.red}Unknown command: "${command}"${c.reset}`);
      showHelp();
      process.exit(1);
  }
}

main().catch((err) => {
  console.error(`\n${c.red}Fatal Error:${c.reset}`, err.message);
  process.exit(1);
});
