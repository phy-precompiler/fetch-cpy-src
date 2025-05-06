""" download files of cpython repository """
# imports
from pathlib import Path
from github import Github

# constants
CPYTHON_REPO_OWNER = 'python'
CPYTHON_REPO_NAME = 'cpython'


def _download_cpython_file(path: str, tag: str, target_dir: Path) -> Path:
    """ download file from cpython repository """
    gh = Github()
    repo = gh.get_repo(f'{CPYTHON_REPO_OWNER}/{CPYTHON_REPO_NAME}')

    # if the remote file does not exists, `github.GithubException.UnknownObjectException` would raise
    file_content = repo.get_contents(path, ref=tag)

    # save it to target directory
    target_path = target_dir / file_content.name
    with target_path.open('w+', encoding='utf8') as _f:
        _f.write(file_content.decoded_content.decode('utf8'))

    return target_path
    
