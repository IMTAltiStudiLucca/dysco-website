# DYSCO website

Website of the DYSCO research unit (Dynamical Systems, Control, and Optimization) at the IMT School for Advanced Studies Lucca.

The site is one scrolling page in plain static HTML and CSS, with a sticky menu. It uses no CDN, external font or framework, and a tiny script only to highlight the current menu item. The text lives in `content/`, and a small Python script (standard library only) turns it into the HTML pages.

## Editing the site

1. Edit or add files in `content/` (see below).
2. Run `python3 build.py`. This rewrites the single page `index.html`.
3. Open `index.html` in a browser to check, then commit the content changes **and** the regenerated `.html` files. GitHub Pages serves the committed HTML.

Never edit the generated `.html` files by hand, since the next build overwrites them. The build also writes `sitemap.xml` and `robots.txt`.

Run `python3 check_links.py` now and then. It lists broken external links found in `content/`. Set the real address of the site in `site_url` of `content/site.json`.

## Content folders

| Folder | What it holds |
| --- | --- |
| `content/site.json` | Site name, address, email, phone, navigation, order of the people groups |
| `content/people/` | One `.md` file per person, photos in `content/people/photos/` |
| `content/research/` | Everything in the Research section. `topics/` and `applications/` have one file per item, and `collaborations.md`, `spinoff.md` and `research.md` hold the other texts |
| `content/software/` | One file per software package |
| `content/teaching/` | One file per PhD course, with an optional `url` |
| `content/pages/` | Text of Home, COLLab, Join us, Teaching and Contact |
| `content/images/` | Page photos |

Files are listed in alphabetical order of their file name, so prefix them with `01-`, `02-` and so on to control the order.

### Adding a person

Create `content/people/first-last.md`.

```
---
name: Jane Doe
group: PhD Students
role: PhD Student
photo: jane-doe.jpg
website: https://example.org/jane
scholar: https://scholar.google.com/citations?user=XXXX
email: jane.doe@imtlucca.it
---
```

Only `name`, `group` and `role` are required. `group` must be one of the names in `people_groups` in `content/site.json` (Faculty, Postdocs, PhD Students, Alumni). Faculty are shown as cards with a photo (initials if there is none). Groups listed in `people_list_groups` of `content/site.json` (Postdocs, PhD Students, Alumni) are shown as a plain list of names, which link to `website` when it is set, so no photo is needed. Photos go in `content/people/photos/`, ideally 4:5 portrait and about 500 px wide. Inside a group, people are sorted by the optional `order` number, then by surname. To remove someone, delete the file.

### Other files

Every other file has a short block between `---` lines followed by optional text. Text supports paragraphs, `## headings`, `- lists`, `[links](https://...)`, `**bold**` and `*italic*`. Look at an existing file and copy it.

## Scope

There are deliberately no news, events or publication pages, since nobody maintains them.

## Licenses and credits

Code is under the MIT license (see `LICENSE`). The previous version of the site is kept in the `umbertos-version` branch.

- `content/images/san-francesco-from-guinigi.jpg` by Zairon, CC BY 4.0, Wikimedia Commons.
- `content/images/imt-cloister.jpg` is a photo of the San Francesco cloister provided by the group. The photographer is to be confirmed.
- `content/images/mpc-blackboard.jpg` comes from the previous DYSCO website.
- `assets/logo.svg` and `assets/iris-ico.ico` belong to their owners and are not covered by the MIT license. They are currently unused.
