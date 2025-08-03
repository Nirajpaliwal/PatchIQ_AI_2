--- a/PatchIQAI_App/Agent Test Code/buggy_bookstore.py
+++ b/PatchIQAI_App/Agent Test Code/buggy_bookstore.py
@@ -115,7 +115,7 @@
         print(f"Book '{book_title}' not found.")
         return
 
-    if found_book["stock"] > 0:
+    if found_book.get("stock", 0) > 0:
         cart.append(found_book)
         found_book["stock"] -= 1
         print(f"'{book_title}' added to cart.")