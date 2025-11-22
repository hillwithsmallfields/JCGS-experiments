;; experiments towards a new .emacs

(use-package straight
  ;; :custom (straight-use-package-by-default t)
  )

;; (straight-use-package 'use-package)

(straight-use-package-mode 1)

;; (use-package emms
;;   :straight t)

;; (use-package '(emms :fetcher github :repo "emacsmirror/emms")
;;   :straight t)

;; (use-package emms
;;   :straight '(emms :fetcher github :repo "emacsmirror/emms"))

(use-package emms
  :straight '(emms :fetcher github :repo "git@github.com:emacsmirror/emms.git")
  :config (emms-add-directory-tree "~/Music"))
