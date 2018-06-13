from app import create_app

manager, app = create_app('development')

if __name__ == '__main__':
    manager.run()
