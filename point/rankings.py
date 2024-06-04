# class Ranking(TimeStampedModel):
#     id = models.AutoField(primary_key=True)
#     year = models.IntegerField()  # The year the ranking is applicable
#     rank = models.IntegerField()  # The rank for the given year
#     point = models.ForeignKey(Point, on_delete=models.CASCADE)  # Link to the Point model

#     class Meta:
#         db_table = 'ranking'
#         unique_together = ('year', 'rank', 'point')
        
        
