from flask import jsonify, Blueprint

from flask.ext.restful import (Resource, Api, reqparse,
								inputs, fields, abort,
								marshal, marshal_with, url_for)

import models


review_fields = {
	'id': fields.Integer,
	'for_course': fields.String,
	'rating': fields.Integer,
	'comment': fields.String(default=''),
	'created_at': fields.DateTime
}

def review_or_404(review_id):
	try:
		review = models.Review.get(models.Review.id==review_id)
	except models.Review.DoesNotExist:
		abort(404, message="Requested review not exists")
	else:
		return review

def add_course(review):
	review.for_course = url_for('resources.courses.course', id=review.course.id)
	return review


class ReviewList(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'course',
			type=inputs.positive,
			required=True,
			help='No course provided',
			location=['form', 'json']
		)
		self.reqparse.add_argument(
			'rating',
			type=inputs.int_range(1, 5),
			required=True,
			help='No rating provided',
			location=['form', 'json']
		)
		self.reqparse.add_argument(
			'comment',
			type=inputs.positive,
			required=False,
			nullable=True,
			location=['form', 'json'],
			default=''
		)
		super(ReviewList, self).__init__()

	def get(self):
		return {'reviews': [marshal(add_course(review), review_fields)
							for review in models.Review.select()]}

	@marshal_with(review_fields)
	def post(self):
		args = self.reqparse.parse_args()
		review = models.Review.create(**args)
		return add_course(review)


class Review(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'course',
			type=inputs.positive,
			required=True,
			help='No course provided',
			location=['form', 'json']
		)
		self.reqparse.add_argument(
			'rating',
			type=inputs.int_range(1, 5),
			required=True,
			help='No rating provided',
			location=['form', 'json']
		)
		self.reqparse.add_argument(
			'comment',
			type=inputs.positive,
			required=False,
			nullable=True,
			location=['form', 'json'],
			default=''
		)
		super(Review, self).__init__()

	def get(self, id):
		return jsonify({'course': 1, 'rating': 5})

	def put(self, id): 
		return jsonify({'course': 1, 'rating': 5})

	def delete(self, id):
		return jsonify({'course': 1, 'rating': 5})


reviews_api = Blueprint('resources.reviews', __name__)
api = Api(reviews_api)
api.add_resource(
	ReviewList,
	'/reviews',
	endpoint='reviews'
)
api.add_resource(
	Review,
	'/reviews/<int:id>',
	endpoint='review'
)