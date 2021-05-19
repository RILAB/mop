from setuptools import setup, find_packages 
  
with open('requirements.txt') as f: 
    requirements = f.readlines() 
  
long_description = 'Produces bedfile of genomic locations that did or did not map reads sufficiently well. Bed regions are Written to standard out.'

  
setup( 
        name ='mop-bam', 
        version ='0.0.3.2', 
        author ='Silas Tittes', 
        author_email ='silas.tittes@gmail.com', 
        url ='https://github.com/RILAB/mop', 
        description ='Get well-mapped regions from bams', 
        long_description = long_description, 
        long_description_content_type ="text/markdown", 
        license ='GPL-3.0', 
        packages = find_packages(), 
        entry_points ={ 
            'console_scripts': [ 
                'mop = mop.mop:main'
            ] 
        }, 
        classifiers =( 
            "Programming Language :: Python :: 3", 
            "License :: OSI Approved :: MIT License", 
            "Operating System :: OS Independent", 
        ), 
        keywords ='bam files genetics python package', 
        install_requires = requirements, 
        zip_safe = False,
        python_requires='>=3.6'
) 
