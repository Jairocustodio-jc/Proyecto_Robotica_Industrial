
(cl:in-package :asdf)

(defsystem "entrega1_ri-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "ArrayXY" :depends-on ("_package_ArrayXY"))
    (:file "_package_ArrayXY" :depends-on ("_package"))
  ))