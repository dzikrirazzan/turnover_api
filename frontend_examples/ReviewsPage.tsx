// Performance Reviews Page Component
import React, { useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { Card, CardHeader, CardContent, CardTitle } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Plus, Star, TrendingUp, Calendar } from 'lucide-react';

export default function ReviewsPage() {
  useAuth(true);
  const [showForm, setShowForm] = useState(false);

  // Mock data - akan diganti dengan real API calls
  const reviews = [
    {
      id: 1,
      employee_name: 'John Doe',
      employee_id: 101,
      overall_rating: 4.5,
      review_period: 'Q1 2024',
      status: 'completed',
      goals_achievement: 4.2,
      communication_skills: 4.8,
      teamwork: 4.3,
      initiative: 4.6,
      created_at: '2024-01-15',
    },
    {
      id: 2,
      employee_name: 'Jane Smith',
      employee_id: 102,
      overall_rating: 4.1,
      review_period: 'Q1 2024',
      status: 'pending',
      goals_achievement: 4.0,
      communication_skills: 4.5,
      teamwork: 3.8,
      initiative: 4.2,
      created_at: '2024-01-10',
    },
  ];

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'draft':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const renderStarRating = (rating) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;

    for (let i = 0; i < fullStars; i++) {
      stars.push(
        <Star key={i} className="h-4 w-4 fill-yellow-400 text-yellow-400" />
      );
    }

    if (hasHalfStar) {
      stars.push(
        <Star key="half" className="h-4 w-4 fill-yellow-200 text-yellow-400" />
      );
    }

    const remainingStars = 5 - Math.ceil(rating);
    for (let i = 0; i < remainingStars; i++) {
      stars.push(
        <Star key={`empty-${i}`} className="h-4 w-4 text-gray-300" />
      );
    }

    return <div className="flex space-x-1">{stars}</div>;
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Performance Reviews</h1>
        <Button onClick={() => setShowForm(true)} className="flex items-center space-x-2">
          <Plus className="h-4 w-4" />
          <span>New Review</span>
        </Button>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Reviews</p>
                <p className="text-2xl font-bold text-gray-900">24</p>
              </div>
              <Calendar className="h-8 w-8 text-blue-600" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Avg Rating</p>
                <p className="text-2xl font-bold text-gray-900">4.3</p>
              </div>
              <Star className="h-8 w-8 text-yellow-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Completed</p>
                <p className="text-2xl font-bold text-gray-900">18</p>
              </div>
              <TrendingUp className="h-8 w-8 text-green-600" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Pending</p>
                <p className="text-2xl font-bold text-gray-900">6</p>
              </div>
              <Calendar className="h-8 w-8 text-orange-600" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Reviews List */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {reviews.map((review) => (
          <Card key={review.id} className="hover:shadow-md transition-shadow">
            <CardHeader>
              <div className="flex justify-between items-start">
                <div>
                  <CardTitle className="text-lg">{review.employee_name}</CardTitle>
                  <p className="text-sm text-gray-600">ID: {review.employee_id}</p>
                </div>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(review.status)}`}>
                  {review.status.charAt(0).toUpperCase() + review.status.slice(1)}
                </span>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <p className="text-sm font-medium text-gray-700">Review Period</p>
                  <p className="text-sm text-gray-600">{review.review_period}</p>
                </div>

                <div>
                  <p className="text-sm font-medium text-gray-700 mb-2">Overall Rating</p>
                  <div className="flex items-center space-x-2">
                    {renderStarRating(review.overall_rating)}
                    <span className="text-sm font-medium">{review.overall_rating}</span>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-gray-600">Goals Achievement</p>
                    <p className="font-medium">{review.goals_achievement}/5</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Communication</p>
                    <p className="font-medium">{review.communication_skills}/5</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Teamwork</p>
                    <p className="font-medium">{review.teamwork}/5</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Initiative</p>
                    <p className="font-medium">{review.initiative}/5</p>
                  </div>
                </div>

                <div className="pt-2">
                  <Button variant="outline" size="sm" className="w-full">
                    View Details
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Performance Review Form Modal */}
      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <ReviewForm onCancel={() => setShowForm(false)} />
          </div>
        </div>
      )}
    </div>
  );
}

// Performance Review Form Component
const ReviewForm = ({ onCancel }) => {
  const [formData, setFormData] = useState({
    employee: '',
    review_period_start: '',
    review_period_end: '',
    overall_rating: 3,
    goals_achievement: 3,
    communication_skills: 3,
    teamwork: 3,
    initiative: 3,
    strengths: '',
    areas_for_improvement: '',
    goals_next_period: '',
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Submitting review:', formData);
    // API call akan ditambahkan di sini
    onCancel();
  };

  const handleRatingChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const RatingInput = ({ label, field, value }) => (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-2">
        {label}
      </label>
      <div className="flex space-x-2">
        {[1, 2, 3, 4, 5].map((rating) => (
          <button
            key={rating}
            type="button"
            onClick={() => handleRatingChange(field, rating)}
            className={`w-8 h-8 rounded-full border-2 flex items-center justify-center text-sm font-medium transition-colors ${
              value >= rating
                ? 'bg-blue-600 border-blue-600 text-white'
                : 'border-gray-300 text-gray-500 hover:border-blue-300'
            }`}
          >
            {rating}
          </button>
        ))}
      </div>
    </div>
  );

  return (
    <form onSubmit={handleSubmit} className="p-6 space-y-6">
      <h3 className="text-xl font-semibold text-gray-900">New Performance Review</h3>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Employee ID
          </label>
          <input
            type="number"
            value={formData.employee}
            onChange={(e) => setFormData(prev => ({ ...prev, employee: e.target.value }))}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter employee ID"
            required
          />
        </div>

        <div className="grid grid-cols-2 gap-2">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Period Start
            </label>
            <input
              type="date"
              value={formData.review_period_start}
              onChange={(e) => setFormData(prev => ({ ...prev, review_period_start: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Period End
            </label>
            <input
              type="date"
              value={formData.review_period_end}
              onChange={(e) => setFormData(prev => ({ ...prev, review_period_end: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
        </div>
      </div>

      {/* Rating Sections */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <RatingInput 
          label="Overall Rating" 
          field="overall_rating" 
          value={formData.overall_rating} 
        />
        <RatingInput 
          label="Goals Achievement" 
          field="goals_achievement" 
          value={formData.goals_achievement} 
        />
        <RatingInput 
          label="Communication Skills" 
          field="communication_skills" 
          value={formData.communication_skills} 
        />
        <RatingInput 
          label="Teamwork" 
          field="teamwork" 
          value={formData.teamwork} 
        />
        <RatingInput 
          label="Initiative" 
          field="initiative" 
          value={formData.initiative} 
        />
      </div>

      {/* Text Areas */}
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Strengths
          </label>
          <textarea
            value={formData.strengths}
            onChange={(e) => setFormData(prev => ({ ...prev, strengths: e.target.value }))}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={3}
            placeholder="Employee's key strengths and achievements..."
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Areas for Improvement
          </label>
          <textarea
            value={formData.areas_for_improvement}
            onChange={(e) => setFormData(prev => ({ ...prev, areas_for_improvement: e.target.value }))}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={3}
            placeholder="Areas where employee can improve..."
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Goals for Next Period
          </label>
          <textarea
            value={formData.goals_next_period}
            onChange={(e) => setFormData(prev => ({ ...prev, goals_next_period: e.target.value }))}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={3}
            placeholder="Goals and objectives for the next review period..."
          />
        </div>
      </div>

      <div className="flex justify-end space-x-3 pt-4 border-t">
        <Button type="button" variant="outline" onClick={onCancel}>
          Cancel
        </Button>
        <Button type="submit">
          Save Review
        </Button>
      </div>
    </form>
  );
};
