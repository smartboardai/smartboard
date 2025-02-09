FROM python:3.10
WORKDIR /code
RUN ls
COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install g4f






# RUN apt-get -y update && apt-get -y install nginx


# RUN pip install browser_cookie3
# RUN  pip install g4f[webdriver]
# RUN pip install -U g4f
# RUN apt-get update && \
#     apt-get install -y \
#         chromium \
#         chromium-driver \
#     && rm -rf /var/lib/apt/lists/*
# ENV CHROMEDRIVER_PATH /usr/lib/chromium/chromedriver
# ENV CHROME_BIN /usr/bin/chromium-browser
# RUN which chromedriver
# RUN chromedriver --version
# RUN wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip

RUN apt-get update && apt-get install -y \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
#    libgtk-4-1 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    libu2f-udev \
    libvulkan1
 # Chrome instalation 
# RUN curl -LO  https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
# RUN rm google-chrome-stable_current_amd64.deb
# # Check chrome version
# RUN echo "Chrome: " && google-chrome --version











# Remove java
# RUN apt-get -qyy remove openjdk-11-jre-headless
# Cleanup
# RUN rm -rf /var/lib/apt/lists/* /var/cache/apt/* \
#   && apt-get -qyy autoremove \
#   && apt-get -qyy clean


#Install Pandoc
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    texlive \
	texlive-xetex \
	lmodern \
	texlive-fonts-recommended \
	texlive-fonts-extra \
    texlive-lang-arabic \
    && rm -rf /var/lib/apt/lists/*
# Install Pandoc
RUN wget https://github.com/jgm/pandoc/releases/download/2.14/pandoc-2.14-1-amd64.deb && \
    dpkg -i pandoc-2.14-1-amd64.deb && \
    rm pandoc-2.14-1-amd64.deb
# Install Amiri font
RUN wget https://github.com/alif-type/amiri-font/archive/refs/tags/1.000.zip && \
    unzip 1.000.zip -d /usr/share/fonts/ && \
    fc-cache -fv && \
    rm 1.000.zip
# Install Eisvogel template
RUN wget https://github.com/Wandmalfarbe/pandoc-latex-template/releases/download/v2.0.0/Eisvogel-2.0.0.tar.gz && \
    tar -xzvf Eisvogel-2.0.0.tar.gz && \
    mkdir -p /usr/share/pandoc/templates/ && \
    mv eisvogel.latex /usr/share/pandoc/templates/ && \
    rm -rf Eisvogel-2.0.0.tar.gz
# RUN wget https://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz 
# RUN zcat < install-tl-unx.tar.gz | tar xf -
# RUN ls
# RUN pwd
# RUN cd install-tl-20240131
# RUN ls
# RUN pwd
# RUN perl ./install-tl --no-interaction 
# Set the TeX Live root directory
# ENV PATH="/usr/local/texlive/2023/bin/x86_64-linux:$PATH"
# ENV TEXLIVE_ROOT="/usr/local/texlive/2023"
# # Run TeX Live manager update script
# RUN wget https://mirror.ctan.org/systems/texlive/tlnet/update-tlmgr-latest.sh && \
#     sh update-tlmgr-latest.sh -- --upgrade --nox11 && \
#     tlmgr update --self --all
# # Remake the lualatex/fontspec cache
# RUN luaotfload-tool -fu
# # Cleanup unnecessary files
# RUN rm update-tlmgr-latest.sh




# Create a user
# RUN useradd -m -u 1000 user

# USER user

# ENV HOME=/home/user \
#     PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

COPY  . $HOME/app
# RUN bash u.sh

# USER root
# RUN chown -R user /usr/bin/chromedriver

WORKDIR $HOME/app/randapi/randai
# RUN python manage.py makemigrations
# RUN python manage.py migrate

CMD [ "python", "manage.py", "runserver", "0.0.0.0:7860", "--settings=randai.settings" ]