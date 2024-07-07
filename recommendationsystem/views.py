# views.py
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from groups.models import Group, UserGroup
from groups.serializers import GroupListSerializer
import pandas as pd



# class RecommendationSystem(generics.ListAPIView):
#     """
#     Recommendation system for groups
#     """
#     Group.objects.all()
#     serializer_class = GroupListSerializer
#     def get(self, request):
#         try:

#             ################################################################################
#             ###########################SIMILAR GROUPS#######################################
#             # Fetch user groups from the database
#             user_groups_1 = UserGroup.objects.filter(user=self.request.user)
#             user_group_data = [(user_group.group.title, user_group.group.subject) for user_group in user_groups_1]

#             # Concatenate titles and subjects for TF-IDF vectorization
#             user_group_texts = ['{} {}'.format(title, subject) for title, subject in user_group_data]

#             # Fetch all group names and subjects from the database
#             all_groups = Group.objects.all()
#             all_group_texts = ['{} {}'.format(group.title, group.subject) for group in all_groups]

#             # Create TF-IDF vectorizer
#             vectorizer = TfidfVectorizer()

#             # Transform group names and subjects into TF-IDF vectors
#             tfidf_matrix = vectorizer.fit_transform(all_group_texts)

#             # Vectorize joined groups
#             joined_groups_vector = vectorizer.transform(user_group_texts)

#             # Compute similarity between joined groups and all groups
#             similarities = cosine_similarity(joined_groups_vector, tfidf_matrix)

#             # Find the most similar groups
#             similar_indices = similarities.argsort()[:, ::-1]



#             #############################################################################
#             ########################SIMILAR USERS########################################


#             # Fetch all user-group relationships
#             user_groups = UserGroup.objects.all()

#             # Create a dataframe for user-group interactions
#             data = {
#                 'user_id': [ug.user.id for ug in user_groups],
#                 'group_id': [ug.group.id for ug in user_groups]
#             }
#             df = pd.DataFrame(data)

#             # Create a user-group matrix
#             user_group_matrix = df.pivot_table(index='user_id', columns='group_id', aggfunc='size',
#                                                fill_value=0)

#             # Compute cosine similarity between groups
#             group_similarity = cosine_similarity(user_group_matrix.T)

#             # Convert to a DataFrame for easy manipulation
#             group_similarity_df = pd.DataFrame(group_similarity, index=user_group_matrix.columns,
#                                                columns=user_group_matrix.columns)

#             # Get groups the user has joined
#             user = request.user
#             user_groups = user_group_matrix.loc[user.id]
#             joined_groups = user_groups[user_groups > 0].index.tolist()

#             # Calculate scores for groups not yet joined by the user
#             group_scores = group_similarity_df.loc[joined_groups].sum().sort_values(ascending=False)
#             group_scores = group_scores[~group_scores.index.isin(joined_groups)]

#             # Get the top recommended groups
#             recommended_group_ids = group_scores.head(5).index.tolist()
#             recommended_groups = list(Group.objects.filter(id__in=recommended_group_ids))

#             # Serialize the data
#             # serializer = GroupListSerializer(recommended_groups, many=True)





#             #############################################################################

#             # Iterate over similar indices and recommend groups not joined yet
#             for indices in similar_indices:
#                 for index in indices:
#                     group = all_groups[int(index)]
#                     if group not in [user_group.group for user_group in user_groups_1] and group not in recommended_groups :
#                         recommended_groups.append(group)
#                         break

#             # Serialize the data
#             serializer = GroupListSerializer(recommended_groups, many=True)   

#             return Response(serializer.data, status=status.HTTP_200_OK)

#         except UserGroup.DoesNotExist:
#             return Response({'error': 'UserGroup not found'}, status=status.HTTP_404_NOT_FOUND)


class RecommendationSystem(generics.GenericAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupListSerializer

    def get(self, request, *args, **kwargs):
        try:
            ################################################################################
            ###########################SIMILAR GROUPS#######################################
            # Fetch user groups from the database
            user_groups_1 = UserGroup.objects.filter(user=request.user)
            user_group_data = [(user_group.group.title, user_group.group.subject) for user_group in user_groups_1]

            # Concatenate titles and subjects for TF-IDF vectorization
            user_group_texts = ['{} {}'.format(title, subject) for title, subject in user_group_data]

            # Fetch all group names and subjects from the database
            all_groups = Group.objects.all()
            all_group_texts = ['{} {}'.format(group.title, group.subject) for group in all_groups]

            # Create TF-IDF vectorizer
            vectorizer = TfidfVectorizer()

            # Transform group names and subjects into TF-IDF vectors
            tfidf_matrix = vectorizer.fit_transform(all_group_texts)

            # Vectorize joined groups
            joined_groups_vector = vectorizer.transform(user_group_texts)

            # Compute similarity between joined groups and all groups
            similarities = cosine_similarity(joined_groups_vector, tfidf_matrix)

            # Find the most similar groups
            similar_indices = similarities.argsort()[:, ::-1]
            
            #############################################################################
            ########################SIMILAR USERS########################################
            
            # Fetch all user-group relationships
            user_groups = UserGroup.objects.all()

            # Create a dataframe for user-group interactions
            data = {
                'user_id': [ug.user.id for ug in user_groups],
                'group_id': [ug.group.id for ug in user_groups]
            }
            df = pd.DataFrame(data)

            # Create a user-group matrix
            user_group_matrix = df.pivot_table(index='user_id', columns='group_id', aggfunc='size', fill_value=0)

            # Compute cosine similarity between groups
            group_similarity = cosine_similarity(user_group_matrix.T)

            # Convert to a DataFrame for easy manipulation
            group_similarity_df = pd.DataFrame(group_similarity, index=user_group_matrix.columns, columns=user_group_matrix.columns)

            # Get groups the user has joined
            user = request.user
            user_groups = user_group_matrix.loc[user.id]
            joined_groups = user_groups[user_groups > 0].index.tolist()

            # Calculate scores for groups not yet joined by the user
            group_scores = group_similarity_df.loc[joined_groups].sum().sort_values(ascending=False)
            group_scores = group_scores[~group_scores.index.isin(joined_groups)]

            # Get the top recommended groups
            recommended_group_ids = group_scores.head(5).index.tolist()
            recommended_groups = list(Group.objects.filter(id__in=recommended_group_ids))
            
            #############################################################################
            
            # Iterate over similar indices and recommend groups not joined yet
            for indices in similar_indices:
                for index in indices:
                    group = all_groups[int(index)]
                    if group not in [user_group.group for user_group in user_groups_1] and group not in recommended_groups:
                        recommended_groups.append(group)
                        break

            # Serialize the data
            serializer = self.get_serializer(recommended_groups, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except UserGroup.DoesNotExist:
            return Response({'error': 'UserGroup not found'}, status=status.HTTP_404_NOT_FOUND)
