Here is the table of endpoints with the specified attributes based on the information provided:

| Name                             | Method | Endpoint                                     | Parameters          | Body | Response             |
|----------------------------------|--------|----------------------------------------------|---------------------|------|----------------------|
| `PostListCreateAPIView`          | GET    | `<int:pk>/posts/`                            | `pk`: int           | -    | List of posts        |
| `PostListCreateAPIView`          | POST   | `<int:pk>/posts/`                            | `pk`: int           | Post data           | Created post         |
| `PostRetrieveUpdateDestroyAPIView`| GET    | `<int:pk>/posts/<int:P_pk>/`                 | `pk`: int, `P_pk`: int | - | Detailed post        |
| `PostRetrieveUpdateDestroyAPIView`| PATCH  | `<int:pk>/posts/<int:P_pk>/`                 | `pk`: int, `P_pk`: int | Updated post data   | Updated post         |
| `PostRetrieveUpdateDestroyAPIView`| DELETE | `<int:pk>/posts/<int:P_pk>/`                 | `pk`: int, `P_pk`: int | -    | -                    |
| `LikePostAPIView`                | POST   | `<int:pk>/posts/<int:P_pk>/like/`            | `pk`: int, `P_pk`: int | -    | Success message      |
| `UnLikePostAPIView`              | POST   | `<int:pk>/posts/<int:P_pk>/unlike/`          | `pk`: int, `P_pk`: int | -    | Success message      |
| `CommentListCreateAPIView`       | GET    | `<int:pk>/posts/<int:P_pk>/comments/`        | `pk`: int, `P_pk`: int | -    | List of comments     |
| `CommentListCreateAPIView`       | POST   | `<int:pk>/posts/<int:P_pk>/comments/`        | `pk`: int, `P_pk`: int | Comment data        | Created comment      |
| `CommentRetrieveUpdateDestroyAPIView`| GET | `<int:pk>/posts/<int:P_pk>/comments/<int:C_pk>/` | `pk`: int, `P_pk`: int, `C_pk`: int | - | Detailed comment   |
| `CommentRetrieveUpdateDestroyAPIView`| PATCH | `<int:pk>/posts/<int:P_pk>/comments/<int:C_pk>/` | `pk`: int, `P_pk`: int, `C_pk`: int | Updated comment data | Updated comment |
| `CommentRetrieveUpdateDestroyAPIView`| DELETE | `<int:pk>/posts/<int:P_pk>/comments/<int:C_pk>/` | `pk`: int, `P_pk`: int, `C_pk`: int | - | -                  |
| `LikeCommentAPIView`             | POST   | `<int:pk>/comments/<int:C_pk>/like/`         | `pk`: int, `C_pk`: int | -    | Success message      |
| `UnLikeCommentAPIView`           | POST   | `<int:pk>/comments/<int:C_pk>/unlike/`       | `pk`: int, `C_pk`: int | -    | Success message      |
| `ReplyListCreateAPIView`         | GET    | `<int:pk>/posts/<int:P_pk>/comments/<int:C_pk>/replies/` | `pk`: int, `P_pk`: int, `C_pk`: int | - | List of replies |
| `ReplyListCreateAPIView`         | POST   | `<int:pk>/posts/<int:P_pk>/comments/<int:C_pk>/replies/` | `pk`: int, `P_pk`: int, `C_pk`: int | Reply data | Created reply |
| `ReplyRetrieveUpdateDestroyAPIView`| GET | `<int:pk>/posts/<int:P_pk>/comments/<int:C_pk>/replies/<int:R_pk>/` | `pk`: int, `P_pk`: int, `C_pk`: int, `R_pk`: int | - | Detailed reply |
| `ReplyRetrieveUpdateDestroyAPIView`| PATCH | `<int:pk>/posts/<int:P_pk>/comments/<int:C_pk>/replies/<int:R_pk>/` | `pk`: int, `P_pk`: int, `C_pk`: int, `R_pk`: int | Updated reply data | Updated reply |
| `ReplyRetrieveUpdateDestroyAPIView`| DELETE | `<int:pk>/posts/<int:P_pk>/comments/<int:C_pk>/replies/<int:R_pk>/` | `pk`: int, `P_pk`: int, `C_pk`: int, `R_pk`: int | - | - |
| `LikeReplyAPIView`               | POST   | `<int:pk>/replies/<int:R_pk>/like/`          | `pk`: int, `R_pk`: int | -    | Success message      |
| `UnLikeReplyAPIView`             | POST   | `<int:pk>/replies/<int:R_pk>/unlike/`        | `pk`: int, `R_pk`: int | -    | Success message      |

This table summarizes the HTTP methods, endpoints, parameters, body requirements, and expected responses for each endpoint based on your Django project setup. Adjustments might be needed based on your specific implementation details or additional requirements.
