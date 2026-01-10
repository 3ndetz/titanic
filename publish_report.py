import datetime
import hashlib
import os
import shutil

if __name__ == "__main__":
    src = 'dvclive/report.md'
    with open(src, 'r', encoding='utf-8') as f:
        content = f.read()
    ts = datetime.datetime.now().strftime('%d-%m-%Y')
    h = hashlib.md5(datetime.datetime.now().isoformat().encode()).hexdigest()[:8]
    fname = f'Exp-{ts}-{h}.md'
    os.makedirs('docs/docs/experiments', exist_ok=True)
    shutil.copy(src, f'docs/docs/experiments/{fname}')
    title = f'Experiment Report {ts} (Unique ID: {h})'
    CLARIFY_MESSAGE = '''*This report was generated automatically by the DVC Live and saved in the docs because of importance.*

- `params.yaml` section contains experiment initial parameters.
- `metrics.json` contains all logged metrics during training.
- lower sections contain plot images of specific metrics.
'''
    with open(f'docs/docs/experiments/{fname}', 'w', encoding='utf-8') as f:
        f.write(f'---\ntitle: {title}\n---\n\n{CLARIFY_MESSAGE}\n\n' + content)
    print(f'Report published: docs/docs/experiments/{fname}')
