;; experiments towards a new .emacs

(use-package straight)

(straight-use-package-mode 1)

(use-package emms
  :straight '(emms :fetcher github :repo "git@github.com:emacsmirror/emms.git")
  :config (emms-add-directory-tree "~/Music"))
