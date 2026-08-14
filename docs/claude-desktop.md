# Claude Desktop setup, no terminal required

This guide installs humanise in Claude in about five minutes, and it assumes no technical
background at all. If you can download a file and click through a settings screen, you have every
skill this page needs.

Three things to know before you begin:

- **This page covers Claude Desktop (the app) and claude.ai (the website).** They share the same
  screens, so every step below works in both. Claude Code is a separate Anthropic product for
  programmers; if you have never used it, skip anything you see elsewhere that mentions it.
- **humanise is free.** It is open-source software, published under a licence (MIT) that lets
  anyone use it at no cost. Nothing in this setup asks you to pay, subscribe or create an
  account, and Anthropic's documentation says skills work on every Claude plan, including Free.
- **Nothing is installed on your computer.** You download one file and hand it to Claude. Claude
  keeps it; your computer runs nothing new.

Do the setup on a computer rather than a phone or tablet: you need to download a file and pick it
from a folder, which is clumsy on a small screen.

Comfortable with a terminal instead? The [complete getting-started guide](getting-started.md)
covers Claude Code and every other host.

## What a skill actually is

A skill is a set of written instructions Claude consults when your request matches what the skill
is for, like handing Claude a reference guide it reads before answering. humanise is one skill: it
teaches Claude to protect your meaning, drop the stock AI phrasing and, over time, learn how you
write. It cannot see your files, does not run in the background, and does not send your writing
anywhere; it is text Claude reads.

## Before you start

You will use two different screens inside Claude. You start in **Settings** for one switch, then
spend the rest of the guide in **Skills**. They are separate places, and each step names which one
you are in.

Claude accepts skill uploads only when its own "Code execution and file creation" feature is on.
That switch belongs to Claude rather than to humanise: it is what lets Claude open and follow the
files inside any skill. Turning it on does not install anything or start anything running on your
computer.

1. In Claude, open **Settings**: click your initials or profile picture at the bottom of the
   sidebar, then choose **Settings**, then **Capabilities**. On the claude.ai website you can also jump straight
   there: [claude.ai/settings/capabilities](https://claude.ai/settings/capabilities). The app and
   the website share one account, so sign in with your usual details and a switch turned on in
   either place applies to both.
2. Make sure **Code execution and file creation** is switched on. If it is off, click the switch
   once. If it is already on, change nothing and move on to Step 1 below.

On a work account (Team or Enterprise), an administrator controls this switch under Organization
settings; ask them to enable Skills and code execution. On a personal account, if you cannot find
the switch anywhere, check Anthropic's
[current skills guide](https://support.claude.com/en/articles/12512180-using-skills-in-claude),
which tracks where the setting lives and which plans include it.

## Step 1: download humanise

Click this link:
[humanise-claude-desktop.zip](https://github.com/Nisus74/humanise/releases/download/claude-desktop-v1/humanise-claude-desktop.zip).

- Your browser saves the file to your **Downloads** folder and lists it in its downloads panel,
  the arrow or file icon near the top of the browser window. Give it a few seconds to finish.
- The file ends in `.zip`, which means one packaged file with the whole skill inside. **Leave it
  exactly as it downloaded.** There is no need to open, unpack or rename it; in Step 3 you hand
  the whole package to Claude, and Claude unpacks it itself.
- If your browser shows a caution message, that is its standard notice for any file from the
  internet. This one comes straight from humanise's official release page, so choose to keep it.
- On a Mac, the system sometimes opens the download into a plain folder by itself. That is fine:
  the original ending in `.zip` is still in Downloads, and that is the one you will use.

## Step 2: open the Skills screen

Go back to Claude. In the sidebar, the column of options along the left edge of the window, click
**Customize**, then the **Skills** tab. This screen lists skills; some built-in ones from
Anthropic may already be there, which is normal, and humanise will join them. You will come back
to this same screen whenever you want to switch humanise off.

## Step 3: upload the zip

1. On the Skills screen, click the **+** button, usually near the top of the skills list.
2. Choose **Create skill**, then **Upload a skill**.
3. A file window opens. Open your **Downloads** folder and select **humanise-claude-desktop**.
   On Windows the `.zip` ending is usually hidden, so it appears as one item with a zip fastener
   on its icon; that item is the right one. On a Mac, if a plain folder appeared beside the
   download, pick the item whose name ends in `.zip`. If you cannot see it at all, type
   "humanise" into the file window's search box.
4. Claude unpacks the file and adds the skill. When it finishes, **humanise** appears in your
   Skills list. It is listed under its skill name, so look for "humanise" rather than the longer
   file name you downloaded.

## Step 4: turn it on

New skills usually switch on by themselves. Check that the switch beside **humanise** in the
Skills list is on; an on switch shows filled or highlighted rather than grey. If it is off, click
it once.

## Step 5: check it worked

Start a new chat, then select and copy the whole message below into it. Before sending, replace
the line in square brackets with a paragraph you actually wrote, such as a sent email or a few
sentences from a document.

```text
Do you have a skill called humanise? If yes, use it to rewrite the text below so it reads less
like AI wrote it. If you cannot find the skill, say so plainly.

[replace this line with your own paragraph]
```

The message asks Claude directly because a rewrite alone proves nothing; Claude can improve text
without any skill installed. The direct question is the real test.

- **Installed:** Claude confirms it has humanise, often showing a brief note that it is reading
  the skill's files, then rewrites your paragraph.
- **Not installed:** Claude says it cannot find a skill called humanise. Go to Troubleshooting
  below.

## Get a result straight away

humanise works from sensible defaults the first time you use it: rewrites arrive with no setup.
The voice profile in the next section is optional, and it only sharpens later results.

## Personalise it

Once a generic rewrite is useful, you can teach humanise your own voice. In any chat, say:

```text
Use humanise in init mode to set up my voice profile.
```

Claude asks for one short piece of your real writing, an email you were happy with is perfect,
offers a few rewritten directions, and saves your choices as a small voice profile. The whole
thing is a conversation; you never edit a file. Sending the sample is an ordinary chat message,
covered by the same Claude privacy settings as anything else you type; humanise keeps what it
learns inside the skill's own profile and sends it nowhere further. Leave out anything
confidential, as you would in any chat.

One caveat before you invest time here. The profile is saved into the skill's own storage, and we
have not yet confirmed that Claude Desktop and claude.ai keep those saved files from one
conversation to the next. If a later chat cannot find your profile and offers to start again, you
have hit that open question; you did nothing wrong, and rewrites keep working either way. Whatever
you observe, we would like to hear about it on the
[project's issues page](https://github.com/Nisus74/humanise/issues); posting there needs a free
GitHub account.

## Troubleshooting

### I can't find Customize or the Skills screen

Look along the left edge of the Claude window for the sidebar. **Customize** sits there, and
**Skills** is a tab inside it. Remember this is a different place from **Settings**, which you
only needed in "Before you start". Claude's menus are occasionally renamed; Anthropic's
[skills guide](https://support.claude.com/en/articles/12512180-using-skills-in-claude) always
shows the current path.

### There's no "Upload a skill" option

Open [claude.ai/settings/capabilities](https://claude.ai/settings/capabilities) (or **Settings >
Capabilities** in the app) and confirm **Code execution and file creation** is on. On a work
account, ask your administrator to enable Skills, since that control sits with them. On a
personal account with no such switch anywhere, Anthropic's
[skills guide](https://support.claude.com/en/articles/12512180-using-skills-in-claude) shows
where the setting currently lives and which plans include it.

### I can't find the file I downloaded

Downloads land in your **Downloads** folder: open Finder and click **Downloads** on a Mac, or
open File Explorer and click **Downloads** on Windows. Your browser's downloads panel, the arrow
or file icon near the top of the window, also lists it. In any file window, typing "humanise" into
the search box finds it.

### My computer opened the download into a folder

This is a Mac habit: it unpacks the download for you but keeps the original. Upload the copy
whose name ends in `.zip`; it is still in Downloads beside the plain folder. If no `.zip` copy
remains, click the Step 1 link again and, this time, leave the new download untouched. Windows
does not unpack downloads by itself, so on Windows the single downloaded item is always the
right one.

### The upload failed, or humanise never appeared in the list

Download a fresh copy from the Step 1 link and try the upload again with that exact file. A
duplicate like `humanise-claude-desktop (1).zip` from downloading twice is safe to use. If the
upload keeps failing, tell us on the
[project's issues page](https://github.com/Nisus74/humanise/issues) and include the message
Claude showed.

### humanise is listed but Claude doesn't seem to use it

Check its switch is on in **Customize > Skills**, then start a new chat and ask for it by name:
"Use the humanise skill to rewrite this." The Step 5 message settles whether it is installed at
all.

### The rewrite doesn't look any different

Give Claude more to work with: a full paragraph, who will read it, and what you want the writing
to achieve. A one-line request gives the skill very little to change.

## Turning it off or removing it

Nothing here is permanent. On the **Customize > Skills** screen, the switch beside humanise turns
it off; an off skill does nothing at all. To remove it completely, click the **...** button beside
that switch, choose **Delete**, and confirm. The zip in your Downloads folder is only the
delivery package: keeping or deleting it has no effect on the installed skill, so once humanise
shows in your Skills list you can treat that file like any other download.

## You're done

That is the whole setup; there is nothing else to configure. If you also use a programmer tool
such as Claude Code or Codex, the [getting-started guide](getting-started.md) covers installing
humanise there, and [Voice setup](SETUP.md) deepens your profile once one exists.
