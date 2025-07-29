import pytest
from unittest.mock import Mock, MagicMock, patch
from sqlalchemy.orm import Session
from app.services.user_service import UserService
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


@pytest.fixture
def mock_db():
    """Mock database session fixture."""
    return Mock(spec=Session)


@pytest.fixture
def user_service(mock_db):
    """UserService instance with mocked database."""
    return UserService(mock_db)


@pytest.fixture
def sample_user_create():
    """Sample UserCreate data for testing."""
    return UserCreate(
        email="test@example.com",
        username="testuser",
        password="testpassword123",
        first_name="Test",
        last_name="User",
        is_active=True
    )


@pytest.fixture
def sample_user_update():
    """Sample UserUpdate data for testing."""
    return UserUpdate(
        email="updated@example.com",
        first_name="Updated",
        last_name="Name"
    )


@pytest.fixture
def sample_user_model():
    """Sample User model instance for testing."""
    user = User()
    user.id = 1
    user.email = "test@example.com"
    user.username = "testuser"
    user.hashed_password = "hashed_password_123"
    user.first_name = "Test"
    user.last_name = "User"
    user.is_active = True
    user.is_superuser = False
    return user


class TestUserService:
    """Test suite for UserService class."""

    def test_init(self, mock_db):
        """Test UserService initialization."""
        service = UserService(mock_db)
        assert service.db == mock_db

    @patch('app.services.user_service.get_password_hash')
    def test_create_user_success(self, mock_hash, user_service, mock_db, sample_user_create):
        """Test successful user creation."""
        # Arrange
        mock_hash.return_value = "hashed_password_123"
        mock_user = Mock(spec=User)
        mock_user.id = 1
        
        # Mock database operations
        mock_db.add = Mock()
        mock_db.commit = Mock()
        mock_db.refresh = Mock()
        
        # Mock User constructor to return our mock user
        with patch('app.services.user_service.User', return_value=mock_user):
            # Act
            result = user_service.create_user(sample_user_create)
        
        # Assert
        mock_hash.assert_called_once_with("testpassword123")
        mock_db.add.assert_called_once_with(mock_user)
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(mock_user)
        assert result == mock_user

    def test_get_user_by_id_found(self, user_service, mock_db, sample_user_model):
        """Test getting user by ID when user exists."""
        # Arrange
        mock_query = Mock()
        mock_filter = Mock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = sample_user_model
        
        # Act
        result = user_service.get_user_by_id(1)
        
        # Assert
        mock_db.query.assert_called_once_with(User)
        assert result == sample_user_model

    def test_get_user_by_id_not_found(self, user_service, mock_db):
        """Test getting user by ID when user doesn't exist."""
        # Arrange
        mock_query = Mock()
        mock_filter = Mock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = None
        
        # Act
        result = user_service.get_user_by_id(999)
        
        # Assert
        mock_db.query.assert_called_once_with(User)
        assert result is None

    def test_get_user_by_email_found(self, user_service, mock_db, sample_user_model):
        """Test getting user by email when user exists."""
        # Arrange
        mock_query = Mock()
        mock_filter = Mock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = sample_user_model
        
        # Act
        result = user_service.get_user_by_email("test@example.com")
        
        # Assert
        mock_db.query.assert_called_once_with(User)
        assert result == sample_user_model

    def test_get_user_by_email_not_found(self, user_service, mock_db):
        """Test getting user by email when user doesn't exist."""
        # Arrange
        mock_query = Mock()
        mock_filter = Mock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = None
        
        # Act
        result = user_service.get_user_by_email("nonexistent@example.com")
        
        # Assert
        mock_db.query.assert_called_once_with(User)
        assert result is None

    def test_get_user_by_username_found(self, user_service, mock_db, sample_user_model):
        """Test getting user by username when user exists."""
        # Arrange
        mock_query = Mock()
        mock_filter = Mock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = sample_user_model
        
        # Act
        result = user_service.get_user_by_username("testuser")
        
        # Assert
        mock_db.query.assert_called_once_with(User)
        assert result == sample_user_model

    def test_get_user_by_username_not_found(self, user_service, mock_db):
        """Test getting user by username when user doesn't exist."""
        # Arrange
        mock_query = Mock()
        mock_filter = Mock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = None
        
        # Act
        result = user_service.get_user_by_username("nonexistent")
        
        # Assert
        mock_db.query.assert_called_once_with(User)
        assert result is None

    @patch('app.services.user_service.verify_password')
    def test_authenticate_user_success(self, mock_verify, user_service, sample_user_model):
        """Test successful user authentication."""
        # Arrange
        mock_verify.return_value = True
        user_service.get_user_by_username = Mock(return_value=sample_user_model)
        
        # Act
        result = user_service.authenticate_user("testuser", "testpassword123")
        
        # Assert
        user_service.get_user_by_username.assert_called_once_with("testuser")
        mock_verify.assert_called_once_with("testpassword123", "hashed_password_123")
        assert result == sample_user_model

    @patch('app.services.user_service.verify_password')
    def test_authenticate_user_user_not_found(self, mock_verify, user_service):
        """Test authentication when user doesn't exist."""
        # Arrange
        user_service.get_user_by_username = Mock(return_value=None)
        
        # Act
        result = user_service.authenticate_user("nonexistent", "password")
        
        # Assert
        user_service.get_user_by_username.assert_called_once_with("nonexistent")
        mock_verify.assert_not_called()
        assert result is None

    @patch('app.services.user_service.verify_password')
    def test_authenticate_user_wrong_password(self, mock_verify, user_service, sample_user_model):
        """Test authentication with wrong password."""
        # Arrange
        mock_verify.return_value = False
        user_service.get_user_by_username = Mock(return_value=sample_user_model)
        
        # Act
        result = user_service.authenticate_user("testuser", "wrongpassword")
        
        # Assert
        user_service.get_user_by_username.assert_called_once_with("testuser")
        mock_verify.assert_called_once_with("wrongpassword", "hashed_password_123")
        assert result is None

    @patch('app.services.user_service.get_password_hash')
    def test_update_user_success(self, mock_hash, user_service, mock_db, sample_user_model, sample_user_update):
        """Test successful user update."""
        # Arrange
        mock_hash.return_value = "new_hashed_password"
        user_service.get_user_by_id = Mock(return_value=sample_user_model)
        mock_db.commit = Mock()
        mock_db.refresh = Mock()
        
        # Act
        result = user_service.update_user(1, sample_user_update)
        
        # Assert
        user_service.get_user_by_id.assert_called_once_with(1)
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(sample_user_model)
        assert result == sample_user_model
        assert sample_user_model.email == "updated@example.com"
        assert sample_user_model.first_name == "Updated"
        assert sample_user_model.last_name == "Name"

    @patch('app.services.user_service.get_password_hash')
    def test_update_user_with_password(self, mock_hash, user_service, mock_db, sample_user_model):
        """Test user update with password change."""
        # Arrange
        mock_hash.return_value = "new_hashed_password"
        user_service.get_user_by_id = Mock(return_value=sample_user_model)
        mock_db.commit = Mock()
        mock_db.refresh = Mock()
        
        user_update = UserUpdate(password="newpassword123")
        
        # Act
        result = user_service.update_user(1, user_update)
        
        # Assert
        mock_hash.assert_called_once_with("newpassword123")
        assert sample_user_model.hashed_password == "new_hashed_password"
        assert result == sample_user_model

    def test_update_user_not_found(self, user_service):
        """Test updating non-existent user."""
        # Arrange
        user_service.get_user_by_id = Mock(return_value=None)
        sample_user_update = UserUpdate(email="test@example.com")
        
        # Act
        result = user_service.update_user(999, sample_user_update)
        
        # Assert
        user_service.get_user_by_id.assert_called_once_with(999)
        assert result is None

    def test_delete_user_success(self, user_service, mock_db, sample_user_model):
        """Test successful user deletion."""
        # Arrange
        user_service.get_user_by_id = Mock(return_value=sample_user_model)
        mock_db.delete = Mock()
        mock_db.commit = Mock()
        
        # Act
        result = user_service.delete_user(1)
        
        # Assert
        user_service.get_user_by_id.assert_called_once_with(1)
        mock_db.delete.assert_called_once_with(sample_user_model)
        mock_db.commit.assert_called_once()
        assert result is True

    def test_delete_user_not_found(self, user_service, mock_db):
        """Test deleting non-existent user."""
        # Arrange
        user_service.get_user_by_id = Mock(return_value=None)
        
        # Act
        result = user_service.delete_user(999)
        
        # Assert
        user_service.get_user_by_id.assert_called_once_with(999)
        mock_db.delete.assert_not_called()
        mock_db.commit.assert_not_called()
        assert result is False

    def test_get_users(self, user_service, mock_db):
        """Test getting list of users with pagination."""
        # Arrange
        mock_users = [Mock(spec=User), Mock(spec=User), Mock(spec=User)]
        mock_query = Mock()
        mock_offset = Mock()
        mock_limit = Mock()
        
        mock_db.query.return_value = mock_query
        mock_query.offset.return_value = mock_offset
        mock_offset.limit.return_value = mock_limit
        mock_limit.all.return_value = mock_users
        
        # Act
        result = user_service.get_users(skip=10, limit=20)
        
        # Assert
        mock_db.query.assert_called_once_with(User)
        mock_query.offset.assert_called_once_with(10)
        mock_offset.limit.assert_called_once_with(20)
        mock_limit.all.assert_called_once()
        assert result == mock_users

    def test_get_users_default_params(self, user_service, mock_db):
        """Test getting list of users with default pagination parameters."""
        # Arrange
        mock_users = [Mock(spec=User)]
        mock_query = Mock()
        mock_offset = Mock()
        mock_limit = Mock()
        
        mock_db.query.return_value = mock_query
        mock_query.offset.return_value = mock_offset
        mock_offset.limit.return_value = mock_limit
        mock_limit.all.return_value = mock_users
        
        # Act
        result = user_service.get_users()
        
        # Assert
        mock_db.query.assert_called_once_with(User)
        mock_query.offset.assert_called_once_with(0)
        mock_offset.limit.assert_called_once_with(100)
        assert result == mock_users
