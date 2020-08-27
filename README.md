# Mining Subjective Subgraph Patterns
This repository contains the combined code of SSG, SIMP, DSSG and DSIMP

<main>

<article id="content">

<header>

# `Mining Subjective Subgraph Patterns`

</header>

<section id="section-intro">This project contains the implementation of SSG, SIMP, DSSG and DSIMP algorithms. Depending upon the usage kindly cite the following papers:

<div>`**SSG:** ﻿

<pre class="print">@Article{vanLeeuwen2016,
	author={van Leeuwen, Matthijs and De Bie, Tijl and 
			Spyropoulou, Eirini and Mesnage, C{\'e}dric},
	title={Subjective interestingness of subgraph patterns},
	journal={Machine Learning},
	year={2016},
	month={Oct},
	day={01},
	volume={105},
	number={1},
	pages={41-75},
	issn={1573-0565},
	doi={10.1007/s10994-015-5539-3},
	url={https://doi.org/10.1007/s10994-015-5539-3}} </pre>

</div>

<div>`**SIMP:** ﻿

<pre class="print">@Article{Kapoor2020a,
	author={Kapoor, Sarang and Saxena, Dhish Kumar
			and van Leeuwen, Matthijs},
	title={Discovering subjectively interesting multigraph patterns},
	journal={Machine Learning},
	year={2020},
	month={Aug},
	day={01},
	volume={109},
	number={8},
	pages={1669-1696},
	doi={10.1007/s10994-020-05873-9},
	url={https://doi.org/10.1007/s10994-020-05873-9}} </pre>

</div>

<div>`**DSSG:** ﻿

<pre class="print">@Article{Kapoor2020b,
	author={Kapoor, Sarang and Saxena, Dhish Kumar
			and van Leeuwen, Matthijs},
	title={Online Summarization of Dynamic Graphs using 
		Subjective Interestingness for Sequential Data}},
	journal={Data Mining and Knowledge Discovery},
	year={Accepted},
	month={In press}} </pre>

</div>

<div>`**DSIMP:** ﻿`</div>

</section>

<section>

</section>

To run the code pre-requites are:

<pre> 

*   Python 3.6

*   [Networkx](https://networkx.github.io/)

*   [Ray](https://github.com/ray-project/ray)

*   Pandas

</pre>

<section>To run the code excute the corresponding Algorithm file in the directory 'src/Algorithms' with required configuration file name passed in the arguments. For example:

<pre> 
		```console
		:~MiningSubjectiveSubgraphPatterns$ python src/Algorithms/SSG.py SSG.ini
		```
	</pre>

The file SSG.ini shall be found in directory 'Confs'.</section>

<section>For any queries kindly write an email to [sarang.iitr@gmail.com](mailto:sarang.iitr@gmail.com)</section>

</article>

<nav id="sidebar">

</nav>

</main>

<footer id="footer">

© 2020 Copyright <cite>Sarang Kapoor</cite>.

</footer>