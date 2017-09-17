aws iam create-user --user-name johnny-pi
aws iam create-access-key --user-name johnny-pi
aws iam attach-user-policy --user-name johnny-pi --policy-arn arn:aws:iam::aws:policy/AmazonPollyReadOnlyAccess
aws iam attach-user-policy --user-name johnny-pi --policy-arn arn:aws:iam::aws:policy/AmazonRekognitionReadOnlyAccess
