# myabi-ecm-logging
The Logging documentation for myAbi / ecm

## 1. Install Dependencies
### 1.1 Install Perl
Perl is required for running build scripts.

Download and install Strawberry Perl (https://strawberryperl.com/).
Verify installation by opening Command Prompt and running:

```bash
perl -v
```

### 1.2 Install MiKTeX and latexmk
MiKTeX is required for building LaTeX documents, and latexmk helps automate the build process.
Download and install MiKTeX.

During installation, ensure the option to install missing packages automatically is enabled.


Open the MiKTeX Console (from the Start menu, doubleclick), go to Packages, search for latexmk, and install it.

Verify installations by running in Command Prompt:

```bash
pdflatex --version
latexmk -v
```

## 2. Clone the Repository

Clone the repository to your local machine:

```bash
git clone git@git.logobject.ch:/data/gitreps/doc-myabi-ecm-logging.git
cd doc-myabi-ecm-logging
```

### 3.3 Install Visual Studio Code (VSCode)
Download and install VSCode.

#### 3.3.1 Install these extensions:
The repo contains a _.vscode_ folder that contain the _setting.json_ and _extentions.json_.
First is used to set the output path of the filed to the _/build_ Folder and latar contain the recommended plugins.

- LaTeX Workshop (LaTeX support, IntelliSense, live PDF preview)
- Perl (Perl script support)
- Project Manager (recommended for managing multiple projects)
- Markdown Preview (recommended for working on the ReadMe file)

#### 3.3.2 Open the project folder in VSCode.
- Open doc-myabi-ecm-logging in VSCode
- Add in Project Manager

## 4. Build the Project

### 4.1 (recommended) Build in VSCode
**VSCode Build Shortcut**
You can compile the project directly inside VSCode using LaTeX Workshop:
```
Ctrl + Alt + B
```
(or use the LaTeX Workshop sidebar "Build LaTeX project" button)

**Output Directory**
The build path in VSCode is set to:
```
./build
```
All generated files (PDF, logs, aux files, …) will be placed there.

### 4.2 Build using Perl
You can build the project using the provided Perl script:
```bash
perl build.pl
```

The build artifacts (such as the generated PDF) are located in the build/ folder:

build/
 └─ main.pdf

## 5. Changes 
### 5.1 Branches
Currently the master is the only Branch. As soon as the Doc is completed as the default doc, we can create Branches for each Customer who need custom docs or languages...

### 5.2 Push Changes
After making changes and building:

```bash
git add .
git commit -m "Your commit message"
git push origin main
```