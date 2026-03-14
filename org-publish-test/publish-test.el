(require 'ox-publish)
;; initially based on https://orgmode.org/worg/org-tutorials/org-publish-html-tutorial.html

(setq org-publish-project-alist nil)

(cl-pushnew '("publishing-test"
              :components ("notes" "static"))
            org-publish-project-alist)
(cl-pushnew '("notes"
              :base-directory "~/open-projects/github.com/hillwithsmallfields/JCGS-experiments/org-publish-test/"
              :base-extension "org"
              :with-toc nil
              :publishing-directory "~/scratch/test-published/"
              :recursive t
              :publishing-function org-html-publish-to-html
              :headline-levels 4
              :auto-preamble t)
            org-publish-project-alist)
(cl-pushnew '("static"
              :base-directory "~/open-projects/github.com/hillwithsmallfields/JCGS-experiments/org-publish-test/"
              :base-extension "css\\|js\\|png\\|jpg\\|gif\\|pdf\\|mp3\\|ogg\\|swf"
              :publishing-directory "~/scratch/test-published/"
              :recursive t
              :publishing-function org-publish-attachment)
            org-publish-project-alist)
      
